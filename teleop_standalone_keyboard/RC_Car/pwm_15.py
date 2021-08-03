from pynput import keyboard
import time
MIN_SPEED = 0
SPEED_STEP = 1
MAX_SPEED = 10
class VechicleControl():

    def __init__(self):
        self.terminate = False
        self.speed = MIN_SPEED
        self.direction = 'center'       
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
    
    def start(self):
        while not self.terminate:

            #with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            #    listener.join()           
            print(self.speed)
            print(self.direction)
    
    def speed_up(self):
        self.speed = min(self.speed + SPEED_STEP, MAX_SPEED)
        #print(self.speed)
    
    def speed_down(self):
        self.speed = max(self.speed - SPEED_STEP, MIN_SPEED)
        
    def neutral(self):
        #print(self.speed)
        return
        
    def left(self):
        self.direction = 'left'
        #print('left')
    
    def right(self):
        self.direction = 'right'
        
    
    def center(self):
        self.direction = 'center'
        
    def on_release(self, key):        
        self.center()
        self.neutral()
        
    def on_press(self, key):
        
        if key == keyboard.Key.esc:
            self.terminate = True
            print('Goodbye')
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
                

        if k == 'up':
            self.speed_up()
        elif k == 'down':
            self.speed_down()
 
            
        if k == 'right':
            self.right()
        elif k == 'left':
            self.left()


V = VechicleControl()
V.start()