import motor
import time
import hub
import color_sensor
from hub import port, motion_sensor # imports for the robot

motion_sensor.reset_yaw(0) # resets yaw to 0 for the compass code to adjust to this yaw

IR = hub.port.E # defines what port the IR ring is in
BaseSpeed = 550

def drive(f, d, a, c): # defines drive with the 4 different motor ports
    mx = max(abs(f), abs(d), abs(a), abs(c))
    if mx > 1000: # this scales the speed down and caps it to 1000 deg/s using //
        f = f * 1000 // mx 
        d = d * 1000 // mx
        a = a * 1000 // mx
        c = c * 1000 // mx

    motor.run(port.F, f) # sends the speed to the motors (after being scaled)
    motor.run(port.D, d) # sends the speed to the motors (after being scaled)
    motor.run(port.A, a) # sends the speed to the motors (after being scaled)
    motor.run(port.C, c) # sends the speed to the motors (after being scaled)

def rotate(rotat):
    drive(rotat, rotat, rotat, rotat)

def Fowards(rotat): # forwards definition
    drive(-BaseSpeed + rotat, BaseSpeed + rotat, BaseSpeed + rotat, -BaseSpeed + rotat)

def Backwards(rotat): # backwards definition
    drive(BaseSpeed + rotat, -BaseSpeed + rotat, -BaseSpeed + rotat, BaseSpeed + rotat)

def Right(rotat): # right definition
    drive(-BaseSpeed + rotat, -BaseSpeed + rotat, BaseSpeed + rotat, BaseSpeed + rotat)

def Left(rotat): # left definition
    drive(BaseSpeed + rotat, BaseSpeed + rotat, -BaseSpeed + rotat, -BaseSpeed + rotat)

def FrontRight(rotat): # front-right definition
    drive(-BaseSpeed + rotat, rotat, BaseSpeed + rotat, rotat)

def FrontLeft(rotat): # front-left definition
    drive(rotat, BaseSpeed + rotat, rotat, -BaseSpeed + rotat)

def BackRight(rotat): # back-right definition
    spd = BaseSpeed * 1.3
    if spd > 1380: spd = 1380
    drive(rotat, -spd + rotat, rotat, spd + rotat)

def BackLeft(rotat): # back-left definition (they are different to the other ones due to the fact that when travelling diagonally, only two motors spin as opposede to all four
    spd = BaseSpeed * 1.3 # and to compensate for the lost speed of the other two motors, it makes the speed 1.3x higher than base speed to get back field)
    if spd > 1380: spd = 1380
    drive(spd + rotat, rotat, -spd + rotat, rotat)

while True: # makes it so that it runs all the time while the robot is on

    time.sleep_ms(15) # pauses program every 15ms

    data = color_sensor.rgbi(IR) # reads data from the IR sensor port
    ir_value = data[0] if data else 0

    yaw = motion_sensor.tilt_angles() # the compass code which keeps it facing the right direction on the field
    yaw_value = yaw[0] if yaw else 0
    rotat = -yaw_value

    if ir_value in (2, 3, 4, 5, 6):
        back_direction = "Right"
    elif ir_value in (8, 9, 10, 11, 12):
        back_direction = "Left"

    if ir_value == 1: # if the ball is infront of it, the robot has a higher target speed and high acceleration to drive the ball into the goal quickly and precisely
        MaxTarget = 1380
        SpeedStep = 30
    elif ir_value in (2, 12): # however, if the ball is elsewhere, the robot has a lower target speed and slightly slower acceleration
        MaxTarget = 1050
        SpeedStep = 25

    if ir_value == 1: # if the ir ring shows the value as 1, it will use the forward variable
        Fowards(rotat)
    elif ir_value == 2: # if the ir ring shows the value as 2, it will use the front right variable
        FrontRight(rotat)
    elif ir_value == 3: # if the ir ring shows the value as 3, it will use the right variable
        Right(rotat)
    elif ir_value == 4: # if the ir ring shows the value as 4, it will use the back right variable
        BackRight(rotat)
    elif ir_value in (5, 6, 8, 9, 10): # if the ir ring shows the value as 5, 6, 8, 9, 10, it will use the backwards variable
        Backwards(rotat)
    elif ir_value == 7: # if the ir ring shows the value as 7, it will use the back left variable
        BackLeft(rotat)
    elif ir_value == 11: # if the ir ring shows the value as 11, it will use the left variable
        Left(rotat)
    elif ir_value == 12: # if the ir ring shows the value as 12, it will use the front left variable
        FrontLeft(rotat)
    elif ir_value == 0: # stops the robot the second the ball is no longer detected
        MaxTarget = 0
        SpeedStep = -25
