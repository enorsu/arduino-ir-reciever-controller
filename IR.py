import serial
import subprocess
import time, os
import sys
from pynput.keyboard import Key, Controller

# keyboard
keyboard = Controller()

# serial port(this is the default for linux)
serial_port = "/dev/ttyACM0"
username = "vi"

# helper fn
def byt(st: str):
	return bytes(f"{st}\r\n",encoding='utf8')
# checking thing
#unused
def check(readline: bytes, hex: str):
    hex = byt(hex)
    if readline == hex: return True
    if readline == hex.replace(b"8", b"0", 1): return True
    if readline == hex.replace(b"0", b"8", 1): return True
    return False

def root_check():
    return os.geteuid() == 0

def press_and_release(key):
     keyboard.press(key)
     keyboard.release(key)

# executing helper fn	
def execute(args: list, launch_in_kitty = False):
     as_root = root_check()
     if as_root:
          other = ["su", username, "&&"]
          args[0:0] = other
          print(args)
          command = ""
          for item in args:
               command += item + " "
          subprocess.run(command, check=False, text=True, shell=True, capture_output=True)
     elif launch_in_kitty:
          args.insert(0,"--")
          args.insert(0,"kitty")
          subprocess.Popen(args)
          
          return
     else:
          print(args)
          subprocess.Popen(args)
          return

# commands
# replace these with your own
# currently depends on https://github.com/vially/volumectl and https://github.com/altdesktop/playerctl
# and a browser
class Commands:
    # music controls
     def vol_up():
          execute(["volumectl", "up"])
     def vol_down():
          execute(["volumectl", "down"])
     def mute():
          execute(["volumectl", "toggle"])
     def rickroll():
          execute(["librewolf", "https://www.youtube.com/watch?v=XfELJU1mRMg"])
     def next_song():
          execute(["playerctl", "next"])
     def previous_song():
          execute(["playerctl", "previous"])
     def back():
          execute(["playerctl", "position", "10+"])
     def fwd():
          execute(["playerctl", "position", "10-"])
     
     def kb_up():
          press_and_release(Key.up)
     def kb_down():
          press_and_release(Key.down)
     def kb_left():
          press_and_release(Key.left)
     def kb_right():
          press_and_release(Key.right)
     def kb_enter():
          press_and_release(Key.enter)
     def kb_backspace():
          press_and_release(Key.backspace)
          
     def mouse_down():
          mouse.drag(start_y=0, end_y=500, absolute=False, start_x=0, end_x=0)
     def mouse_up():
          mouse.drag(start_y=0, end_y=-500, absolute=False, start_x=0, end_x=0)
     def mouse_right():
          mouse.drag(start_x=0, end_x=500, absolute=False, start_y=0, end_y=0)
     def mouse_left():
          mouse.drag(start_x=0, end_x=-500, absolute=False, start_y=0, end_y=0)
     def left_click():
          mouse.click()
     def one():
          # because yes
          execute(["/home/vi/AppImages/cheatbreaker.appimage"], launch_in_kitty=True)
     def pause():
          execute(["playerctl", "play-pause"])
     # configuration for a Luxor remote
     commands = {
          "1050": vol_up,
          "1051": vol_down,
          "104D": pause,
          "1074": rickroll,
          # for kodi or librelec
          "1054": kb_up,
          "1056": kb_right,
          "1055": kb_left,
          "1053": kb_down,
          "1075": kb_enter,
          "104A": kb_backspace,
          # end
          "1060": next_song,
          "1061": previous_song,
          "106F": back,
          "1052": fwd,
          # 104X where X is the number on the remote
          # for example 1045 is the number five on the remote...
          "1041": one

     }
         
# open the serial port
with serial.Serial(serial_port) as s:
    print(f"Serial listening on port {serial_port} ")
    if root_check(): sys.exit(0)


    while True:
        # reads the latest line from the arduino
        a = s.readline()
        print(str(a))
        # goes through the commands and checks if a command for it exists
        for key, value in Commands.commands.items():
             keybyte = byt(key)
             # the replace thing is just for the specific remote, i have not tested it with other remotes
             if keybyte == a or keybyte.replace(b"0", b"8", 1) == a:

               try:
                    # run the fn
                    value()
               except ImportError as err:
                    # print the error if not running as root
                    print(err)
               print(value)
               break


        
             
             