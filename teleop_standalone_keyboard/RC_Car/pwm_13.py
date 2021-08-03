from pynput import keyboard

    
class VechicleControl():

    def __init__(self):
        self.terminate = False      

    
    def start(self):
        while not self.terminate:

            with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
                listener.join()           

    def on_release(self, key):
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        print(k + ' is released') 

        
    def on_press(self, key):
        
        if key == keyboard.Key.esc:
            self.terminate = True
            print('Goodbye')
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
                
        if k in ['up', 'down', 'left', 'right']:  # keys of interest
            # self.keys.append(k)  # store it in global-like variable
            print('Key pressed: ' + k)
        #return False  # stop listener; remove this if want more keys

V = VechicleControl()
V.start()