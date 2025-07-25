import serial
import subprocess
import mouse
import time

# serial port(this is the default for linux)
serial_port = "/dev/ttyACM0"


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

# executing helper fn	
def execute(args: list, launch_in_kitty = False):
     if launch_in_kitty:
          args.insert(0,"--")
          args.insert(0,"kitty")
          subprocess.Popen(args)
          return
     else:
          subprocess.Popen(args)

# commands
# replace these with your own
# currently depends on https://github.com/vially/volumectl and https://github.com/altdesktop/playerctl
# and a browser
class Commands:
    
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
          "104D": mute,
          "1074": rickroll,
          "1054": mouse_up,
          "1056": mouse_right,
          "1055": mouse_left,
          "1053": mouse_down,
          "1070": left_click,
          "1060": next_song,
          "1061": previous_song,
          "106F": pause,
          # 104X where X is the number on the remote
          # for example 1045 is the number five on the remote...
          "1041": one

     }
         
# open the serial port
with serial.Serial(serial_port) as s:
    print(f"Serial listening on port {serial_port}")
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


        
             
             