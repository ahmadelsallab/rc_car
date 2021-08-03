import keyboard
import time
#declaring it global so that it can be modified from function
global releaseListening
keepListening = True


def key_press(key):
  print(key.name, ' pressed')
  #if escape is pressed make listening false and exit 
  if key.name == "esc":
    keepListening = False
def key_release(key):
  print(key.name, ' released')
  #if escape is pressed make listening false and exit 
  if key.name == "esc":
    keepListening = False
keyboard.on_press(key_press)
keyboard.on_release(key_release, suppress=True)

while keepListening :
  time.sleep(1)