import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO

# Vehicle params
MIN_SPEED = 4
SPEED_STEP = 1
MAX_SPEED = 10

CENTER_ANGLE = 0
MIN_ANGLE = 4
ANGLE_STEP = 4
MAX_ANGLE = 6

# LLC params:
# For pinout RPi 3 Model B, see: https://i.stack.imgur.com/VEBEs.png
THROTTLE_MOT_EN = 18
THROTTLE_MOT_IN1 = 23
THROTTLE_MOT_IN2 = 24

THROTTLE_PWM_FREQ = 1000
MAX_DUTY = 100
MIN_DUTY = 20


STEER_IN1 = 25
STEER_IN2 = 8
STEER_EN = 7
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


class Vechicle(Node):

    def __init__(self):
        super().__init__('vehicle_handler')
        self.terminate = False
        self.speed = 0
        self.angle = CENTER_ANGLE
        self.direction = 'center'
        self.VC = VehicleControl()
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_cbk)
        
        self.message = self.create_subscription(
            Twist,
            'cmd_vel',
            self.message_cbk,
            10)
        self.message      # prevent unused variable warning
        self.msg_rcvd = False
    
    def message_cbk(self, msg):
        self.speed = msg.linear.x
        self.angle = msg.angular.z
        print('cmd_vel params are: ', self.speed, self.angle)
        self.msg_rcvd = True

        
        if self.speed > 0: 
            self.speed_up()
        elif self.speed < 0:
            self.speed_down()
        else:
            self.stop()
            
        
        # cmd_vel msg is invereted
        self.angle *= -1
        if self.angle > 0: 
            self.right()
        elif self.angle < 0:
            self.left()
        else:
            self.center()
        
    def timer_cbk(self):
        print(self.speed)
        print(self.direction, self.angle)
        
        if not self.msg_rcvd:
            self.center()
            #self.stop to execute one command at a time, and self.neutral to continue
            self.stop()
        
        
        self.llc_cmd_throttle(self.speed)
        self.llc_cmd_steer(self.direction, self.angle)
        
        self.msg_rcvd = False

            
    def llc_cmd_throttle(self, speed):
        if speed > 0.0: self.VC.move_fwd(abs(speed))
        elif speed < 0.0: self.VC.move_bwd(abs(speed))
        else: self.VC.stop()
        
    def llc_cmd_steer(self, dir, angle):
        if dir == 'right': self.VC.move_right(abs(angle))
        elif dir == 'left': self.VC.move_left(abs(angle))
        else: self.VC.move_center()
        
    def speed_up(self):
        self.speed = min(self.speed, MAX_SPEED)
        self.speed = max(self.speed, MIN_SPEED)
       
    
    def speed_down(self):
        self.speed = max(self.speed, -MAX_SPEED)
        self.speed = min(self.speed, -MIN_SPEED)
        
    def neutral(self):
        #print(self.speed)
        return
    
    def right(self):
        self.direction = 'right'
        self.angle = min(self.angle, MAX_ANGLE)
        self.angle = max(self.angle, MIN_ANGLE)
        
    def left(self):
        self.direction = 'left'
        self.angle = max(self.angle, -MAX_ANGLE)
        self.angle = min(self.angle, -MIN_ANGLE)
        
    def stop(self):
        self.speed = 0
        #self.center()
        
            
    def center(self):
        self.direction = 'center'
        self.angle = CENTER_ANGLE
        



def main(args=None):
    rclpy.init(args=args)

    V = Vechicle()

    rclpy.spin(V)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    V.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()