import motor
import time
import hub
import color_sensor
from hub import port, motion_sensor
# Variables
SoftCapReduction = 10 # How much speed is removed when the speed reaches the soft cap
SoftCap = 400 # The speed can pass this value but when the value is passed the code reduces the speed by a set amount
Cap = 900 # The speed can not pass this value
Increment = 50 # How much the speed increases for each integer
motion_sensor.reset_yaw(0) # Code that resets the Compass
# Variables for the different motors
D1 = (0)
D2 = (0)
D3 = (0)
D4 = (0)
# Port for the IR Sensor
IR = hub.port.E

def rotate(rotat): # Compass code
    motor.run(port.F, rotat)
    motor.run(port.D, rotat)
    motor.run(port.A, rotat)
    motor.run(port.C, rotat)


while True: # While true loop
    data = color_sensor.rgbi(IR)
    ir_value = data[0] if data else 0
    # Compass code
    yaw = motion_sensor.tilt_angles()
    yaw_value = yaw[0] if yaw else 0
    #Variables
    side = 0 # Backwards Direction
    rotat = -yaw_value # Compass Variable

    motor.run(port.F, D1 + rotat)
    motor.run(port.D, D2 + rotat)
    motor.run(port.A, D3 + rotat)
    motor.run(port.C, D4 + rotat)

#HardCap to stop moving too fast
    if D1 > Cap:
        D1 = Cap
    if D1 < -Cap:
        D1 = -Cap

    if D2 > Cap:
        D2 = Cap
    if D2 < -Cap:
        D2 = -Cap

    if D3 > Cap:
        D3 = Cap
    if D3 < -Cap:
        D3 = -Cap

    if D4 > Cap:
        D4 = Cap
    if D4 < -Cap:
        D4 = -Cap

#SoftCap to give the robot a base speed
    if D1 > SoftCap:
        D1 = D1 - SoftCapReduction
    if D1 < -SoftCap:
        D1 = D1 + SoftCapReduction

    if D2 > SoftCap:
        D2 = D2 - SoftCapReduction
    if D2 < -SoftCap:
        D2 = D2 + SoftCapReduction

    if D3 > SoftCap:
        D3 = D3 - SoftCapReduction
    if D3 < -SoftCap:
        D3 = D3 + SoftCapReduction

    if D4 > SoftCap:
        D4 = D4 - SoftCapReduction
    if D4 < -SoftCap:
        D4 = D4 + SoftCapReduction

#Prints motor values        
    if data:
        print("Data = ", D1 , D2 , D3 , D4 )
    time.sleep_ms(10)

    if ir_value == 1:   #Fowards
        if ir_value ==1:
            time.sleep_ms(10)
            D1 = D1 - Increment
            D2 = D2 + Increment
            D3 = D3 + Increment
            D4 = D4 - Increment
   
    elif ir_value == 7:     #Backwards
        if ir_value == 7:
            time.sleep_ms(10)
            D1 = D1 + Increment
            D2 = D2 - Increment
            D3 = D3 - Increment
            D4 = D4 + Increment
           
    elif ir_value == 2:     #Frontright
        if ir_value == 2:
            time.sleep_ms(10)
            D1 = D1 + 0
            D2 = D2 - Increment
            D3 = D3 + 0
            D4 = D4 + Increment
           
   
    elif ir_value == 12:    #Frontleft
        if ir_value == 12:
            time.sleep_ms(10)
            D1 = D1 + Increment
            D2 = D2 + 0
            D3 = D3 - Increment
            D4 = D4 + 0
       
    elif ir_value == 4:     #Right
        if ir_value == 4:
            time.sleep_ms(10)
            D1 = D1 + 0
            D2 = D2 - Increment
            D3 = D3 + 0
            D4 = D4 + Increment


    elif ir_value == 10:    #Left
        if ir_value == 10:
            time.sleep_ms(10)
            D1 = D1 + Increment
            D2 = D2 + 0
            D3 = D3 - Increment
            D4 = D4 + 0

 
    elif ir_value == 6:     #BackRight
        if ir_value == 6:
            time.sleep_ms(10)
            side = 2
            D1 = D1 + 0
            D2 = D2 - Increment
            D3 = D3 + 0
            D4 = D4 + Increment

    elif ir_value == 8:     #BackLeft
        if ir_value == 8:
            time.sleep_ms(10)
            side = 1
            D1 = D1 + Increment
            D2 = D2 + 0
            D3 = D3 - Increment
            D4 = D4 + 0

    elif ir_value == 7:    #Backwards
        if ir_value == 7:
            time.sleep_ms(10)
            if side == 2: # Backwards directions code
                D1 = D1 + 0
                D2 = D2 - Increment
                D3 = D3 + 0
                D4 = D4 + Increment
            if side == 1:
                D1 = D1 + Increment
                D2 = D2 + 0
                D3 = D3 - Increment
                D4 = D4 + 0    
