# rc_car

This repo is for donkeycar-like RC car, which  custom made by modifying a normal toy RC car. Control on-board is done using Rasperry Pi 3.
Pi-camera teleoperation is "theoritically" possible (See https://github.com/ahmadelsallab/picam). But not reliable, as there's much delay.

Two modes are supported:
- Teleop by listening to  wireless keyboard strokes.
- ROS2 node teleoperation


## ROS2 Node Teleop

### Pi side
Eiher as ROS2 node:
`ros2 run rc_car vechicle`

Or as python script:

`python3 rc_car/rc_car/vehicle.py`

This will subscribe to /cmd_vel topic.

In this mode, the command is executed once, then returns to center direction and speed = 0.
This is almost the same as the [turtlesim tutorial](https://docs.ros.org/en/foxy/Tutorials/Turtlesim/Introducing-Turtlesim.html)

### Remote PC side
Any teleoperation tool, publsihing /cmd_vel is possible. It is possible to remap the topic as follows:

__turtlesim__

`ros2 run turtlesim turtle_teleop_key --ros-args --remap /turtle1/cmd_vel:=/cmd_vel`

```
---------------------------
Use arrow keys to move the turtle.
Use G|B|V|C|D|E|R|T keys to rotate to absolute orientations. 'F' to cancel a rotation.
'Q' to quit.

```


__twist teleop keyboard__

`ros2 run teleop_twist_keyboard teleop_twist_keyboard`
This already publishes /cmd_vel

```
This node takes keypresses from the keyboard and publishes them
as Twist messages. It works best with a US keyboard layout.
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%

```

This node is specifically good, due to diagonal moves (U, O, M, >).


__turtlebot3__

`export TURTLEBOT3_MODEL=burger`

`ros2 run turtlebot3_teleop teleop_keyboard`

```
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)

space key, s : force stop

CTRL-C to quit

```


## Teleop standalone keyboard
__Note that:__

This approach requires Line-of-Sight (LoS), as communication happens assuming wireless keyboard (USB connected to Pi). This is a limitation in case of non LoS, or teleop using camera in remote loccations.

Two approaches were used: https://stackoverflow.com/questions/54524225/keyboard-input-over-ssh-to-the-raspberry-pi3-with-pynput-function-in-python
In the standalone mode, we need to remotely connect to the pi. Using pynput need X-server.
We try to use keyboard: https://pypi.org/project/keyboard/
But you need to:
- sudo pip3 install keyboard
- Run using: sudo python3 pwm_integ_88.py
Pros and cons:
- Pynput.keyboard: 
    - Requires VNC, not possible from terminal
    + Accepts remote keyboard, no need to connect keyboard to Pi. This is extremely useful when there is LoS but we have Wifi or network.
- keyboard:
    + Terminal is possible (sudo)
    - Cannot accept remote keyboard input from VNC.
### Pre-requsites:
`sudo pip3 install keyboard`

### Pi side
`sudo python3 RC_car/pwm_integ_hw_8.py`

### Remote PC side
Just press up, down, right left, s=stop

Note that: in this mode, the speed is mentained, and the last command is given to the actuators. This is another limitation, since it's better to execute one key stroke and stop, specially with LoS limitation (it could be lost and keep moving and hit something).
