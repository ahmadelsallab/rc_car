import keyboard
import string
from threading import *


# I can't find a complete list of keyboard keys, so this will have to do:
keys = list(string.ascii_lowercase)
"""
Optional code(extra keys):

keys.append("space_bar")
keys.append("backspace")
keys.append("shift")
keys.append("esc")
"""
def listen(key):
    while True:
        keyboard.wait(key)
        print("[+] Pressed",key)
threads = [Thread(target=listen, kwargs={"key":key}) for key in keys]
for thread in threads:
    thread.start()