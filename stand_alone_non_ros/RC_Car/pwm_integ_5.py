'''
https://stackoverflow.com/questions/54524225/keyboard-input-over-ssh-to-the-raspberry-pi3-with-pynput-function-in-python
In the standalone mode, we need to remotely connect to the pi. Using pynput need X-server.
We try to use keyboard: https://pypi.org/project/keyboard/

But you need to:
- sudo pip3 install keyboard
- Run using: sudo python3 pwm_integ_4.py

Pros and cons:
- Pynput.keyboard: 
    - Requires VNC, not possible from terminal
    + Accepts remote keyboard, no need to connect keyboard to Pi. This is extremely useful when there is LoS but we have Wifi or network.
- keyboard:
    + Terminal is possible (sudo)
    - Cannot accept remote keyboard input from VNC.
'''
#from pynput import keyboard
import keyboard

import RPi.GPIO as GPIO
import time

# Vehicle params
MIN_SPEED = 0
SPEED_STEP = 1
MAX_SPEED = 10

MIN_ANGLE = 0
ANGLE_STEP = 2
MAX_ANGLE = 10

# LLC params
THROTTLE_MOT_IN1 = 24
THROTTLE_MOT_IN2 = 23
THROTTLE_MOT_EN = 25
THROTTLE_PWM_FREQ = 1000
MAX_DUTY = 100
MIN_DUTY = 20

STEER_EN = 17
STEER_IN1 = 27
STEER_IN2 = 22
STEER_PWM_FREQ = 1000


class VehicleControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(THROTTLE_MOT_IN1,GPIO.OUT)
        GPIO.setup(THROTTLE_MOT_IN2,GPIO.OUT)
        GPIO.setup(THROTTLE_MOT_EN,GPIO.OUT)
        GPIO.output(THROTTLE_MOT_IN1,GPIO.LOW)
        GPIO.output(THROTTLE_MOT_IN2,GPIO.LOW)
        self.thr_en_pwm = GPIO.PWM(THROTTLE_MOT_EN, THROTTLE_PWM_FREQ)
        self.thr_en_pwm.start(MIN_DUTY)
        
        GPIO.setup(STEER_IN1,GPIO.OUT)
        GPIO.setup(STEER_IN2,GPIO.OUT)
        GPIO.setup(STEER_EN,GPIO.OUT)
        GPIO.output(STEER_IN1,GPIO.LOW)
        GPIO.output(STEER_IN2,GPIO.LOW)
        self.steer_en_pwm = GPIO.PWM(STEER_EN, STEER_PWM_FREQ)
        self.steer_en_pwm.start(MIN_DUTY)
    
    def move_fwd(self, speed):
        # Direction
        GPIO.output(THROTTLE_MOT_IN1, GPIO.HIGH)
        GPIO.output(THROTTLE_MOT_IN2, GPIO.LOW)
        # Speed = duty
        self.thr_en_pwm.ChangeDutyCycle(int(speed / MAX_SPEED * MAX_DUTY))
        
        
    def move_bwd(self, speed):
        # Direction
        GPIO.output(THROTTLE_MOT_IN1, GPIO.LOW)
        GPIO.output(THROTTLE_MOT_IN2, GPIO.HIGH)
        
        # Speed = duty
        self.thr_en_pwm.ChangeDutyCycle(int(speed / MAX_SPEED * MAX_DUTY))
    
    def move_right(self, angle):
        # Direction
        GPIO.output(STEER_IN1, GPIO.LOW)
        GPIO.output(STEER_IN2, GPIO.HIGH)
        
        # Angle = duty
        #self.steer_en_pwm.ChangeDutyCycle(50)
        self.steer_en_pwm.ChangeDutyCycle(int(angle / MAX_ANGLE * MAX_DUTY))
        
    def move_left(self, angle):
        # Direction
        GPIO.output(STEER_IN1, GPIO.HIGH)
        GPIO.output(STEER_IN2, GPIO.LOW)
        
        # Angle = duty
        #self.steer_en_pwm.ChangeDutyCycle(50)#(int(speed / MAX_SPEED * MAX_DUTY))
        self.steer_en_pwm.ChangeDutyCycle(int(angle / MAX_ANGLE * MAX_DUTY))
        
    def move_center(self):
        GPIO.output(STEER_IN1, GPIO.LOW)
        GPIO.output(STEER_IN2, GPIO.LOW)
        
    def stop(self):
        GPIO.output(THROTTLE_MOT_IN1, GPIO.LOW)
        GPIO.output(THROTTLE_MOT_IN2, GPIO.LOW)
        
class Vechicle():

    def __init__(self):
        self.terminate = False
        self.speed = MIN_SPEED
        self.angle = MIN_ANGLE
        self.direction = 'center'
        self.VC = VehicleControl()
        #listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        #listener.start()
        keyboard.on_press(self.on_press)
        keyboard.on_release(self.on_release, suppress=True)
    
    def loop(self):
        try:
            while not self.terminate:

                print(self.speed)
                self.llc_cmd_throttle(self.speed)
                
                print(self.direction, self.angle)
                self.llc_cmd_steer(self.direction, self.angle)
                time.sleep(0.5)
        finally:
            GPIO.cleanup()
            
    def llc_cmd_throttle(self, speed):
        if speed > 0.0: self.VC.move_fwd(speed)
        elif speed < 0.0: self.VC.move_bwd(abs(speed))
        else: self.VC.stop()
        
    def llc_cmd_steer(self, dir, angle):
        if dir == 'right': self.VC.move_right(angle)
        elif dir == 'left': self.VC.move_left(angle)
        else: self.VC.move_center()
        
    def speed_up(self):
        self.speed = min(self.speed + SPEED_STEP, MAX_SPEED)
       
    
    def speed_down(self):
        self.speed = max(self.speed - SPEED_STEP, -MAX_SPEED)
        
    def neutral(self):
        #print(self.speed)
        return
    
    def right(self):
        self.direction = 'right'
        self.angle = min(self.angle + ANGLE_STEP, MAX_ANGLE)
        
    def left(self):
        self.direction = 'left'
        self.angle = min(self.angle + ANGLE_STEP, MAX_ANGLE)
        
    def stop(self):
        self.speed = MIN_SPEED
        self.center()
        
            
    def center(self):
        self.direction = 'center'
        self.angle = MIN_ANGLE
        
    def on_release(self, key):        
        self.center()
        self.neutral()
        
    def on_press(self, key):
        
        if key.name == "esc":#keyboard.Key.esc:
            self.terminate = True
            print('Goodbye')
            GPIO.cleanup()
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
                
        
        if k == 'up':
            self.speed_up()
        elif k == 'down':
            self.speed_down()
        elif k == 's':            
            self.stop()
 
            
        if k == 'right':
            self.right()
        elif k == 'left':
            self.left()


V = Vechicle()
V.loop()