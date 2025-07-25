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
def press_shortcut(first, second):
     with keyboard.pressed(first):
          keyboard.press(second)
          keyboard.release(second)


# executing helper fn	
def execute(args: list, launch_in_kitty = False):
     if launch_in_kitty:
          args.insert(0,"--")
          args.insert(0,"kitty")
          subprocess.Popen(args)
          
          return
     else:
          subprocess.Popen(args)
          return


# commands
# replace these with your own
# currently depends on https://github.com/vially/volumectl and https://github.com/altdesktop/playerctl
# and a browser
class Commands:
     

     
     # music controls
     class MusicControls:
          
          
          def vol_up():
               execute(["volumectl", "up"])

          def vol_down():
               execute(["volumectl", "down"])

          def mute():
               execute(["volumectl", "toggle"])


          def next_song():
               execute(["playerctl", "next"])

          def previous_song():
               execute(["playerctl", "previous"])

          def back():
               execute(["playerctl", "position", "10+"])

          def fwd():
               execute(["playerctl", "position", "10-"])
          def pause():
               execute(["playerctl", "play-pause"])

     
     # misc
     class Misc:
          
          def rickroll():
               execute(["librewolf", "https://www.youtube.com/watch?v=XfELJU1mRMg"])
          
     class kbMode:

          enabled = False
          
          def toggle():
               if Commands.kbMode.enabled:
                    Commands.kbMode.enabled = False
               elif not Commands.kbMode.enabled:
                    Commands.kbMode.enabled = True
               print(Commands.kbMode.enabled)
          def get():
               return Commands.kbMode.enabled

     # keyboard related
     class KB:
          def par(key):
               if Commands.kbMode.enabled and key != Key.enter or key != Key.backspace:
                    for i in range(3):
                         press_and_release(key)
                         time.sleep(0.05)
               else:
                    press_and_release(key)
          
          def up():
               Commands.KB.par(Key.up)

          def down():
               Commands.KB.par(Key.down)

          def left():
               Commands.KB.par(Key.left)

          def right():
               Commands.KB.par(Key.right)

          def enter():
               Commands.KB.par(Key.enter)

          def backspace():
               Commands.KB.par(Key.backspace)


     # just some funny things
     class Numbers:
          def one():
               # because yes
               execute(["/home/vi/AppImages/cheatbreaker.appimage"], launch_in_kitty=True)
          def two():
               execute(["kodi"], launch_in_kitty=True)
               
               
          
          def four():
               press_shortcut(Key.alt, Key.f4)
               


     # configuration for a Luxor remote
     commands = {
          
          "1050": MusicControls.vol_up,
          "1051": MusicControls.vol_down,
          "104D": MusicControls.pause,
          "1074": Misc.rickroll,
          "1060": MusicControls.next_song,
          "1061": MusicControls.previous_song,
          "106F": MusicControls.back,
          "1052": MusicControls.fwd,
          
          # for kodi or librelec
          "1054": KB.up,
          "1056": KB.right,
          "1055": KB.left,
          "1053": KB.down,
          "1075": KB.enter,
          "104A": KB.backspace,

          # 104X where X is the number on the remote
          # for example 1045 is the number five on the remote.
          "1041": Numbers.one,
          "1042": Numbers.two,
          "1044": Numbers.four,
          "1078": kbMode.toggle

     }
         
# open the serial port
with serial.Serial(serial_port) as s:
    
    if root_check():
         print("Running as root IS NOT supported!")
         sys.exit(0)
    print(f"Serial listening on port {serial_port} ")

    while True:
        # reads the latest line from the arduino
        a = s.readline()
        print(str(a))
        # goes through the commands and checks if a command for it exists
        for key, value in Commands.commands.items():
             keybyte = byt(key)
             
             # the replace thing is just for the specific remote, i have not tested it with other remotes
             if keybyte == a or keybyte.replace(b"0", b"8", 1) == a:
               # run the fn
               value()

               print(value)
               break


        
             
             