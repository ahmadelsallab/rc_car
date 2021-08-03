from pynput import keyboard
terminate = False
def on_press(key):
    global terminate
    if key == keyboard.Key.esc:
        terminate = True
        print('Goodbye')
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys

while not terminate:
    listener = keyboard.Listener(on_press=on_press)    
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys