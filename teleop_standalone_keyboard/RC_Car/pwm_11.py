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
    #print(k)
    if k in ['up', 'down', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        #return False  # stop listener; remove this if want more keys
def on_release(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    print(k + ' is released')
    
while not terminate:
    
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    
    '''
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    listener.start()
    '''