from pynput import keyboard
terminate = False
def throttle(key):
    global terminate
    if key == keyboard.Key.esc:
        terminate = True
        print('Goodbye')
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    print(k)
    if k in ['up', 'down']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys
    
def steer(key):
    global terminate
    if key == keyboard.Key.esc:
        terminate = True
        print('Goodbye')
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    print(k)
    if k in ['right', 'left']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys    

while not terminate:
    throttle_listener = keyboard.Listener(on_press=throttle)    
    throttle_listener.start()  # start to listen on a separate thread
    #throttle_listener.join()  # remove if main thread is polling self.keys
    
    steer_listener = keyboard.Listener(on_press=steer)
    steer_listener.start()
    #steer_listener.join()