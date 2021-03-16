"41.269250430844856 71.82374207264324 | 42.980050940806315 72.99282382825892 |"

import time

with open("output.txt","r") as r:
    tasks = r.readlines()

temp3 = [] 
for task in tasks:  
    temp2 = []  
    task = task.split(" | ")
    task.pop(-1)
    for angles in task:
        temp = []
        angles = angles.split()
        for angle in angles:
            angle = float(angle)
            temp.append(angle)
        temp2.append(temp)
    temp3.append(temp2)
tasks = temp3

def update_servo(angle,real_servo):
    pwm = angle/18 + 2.5
    real_servo.ChangeDutyCycle(pwm)    

def move_servos(servo_angles, *args):
    timestep = 1/24
    if args:
        timestep = args[0]
    #only considering 2 servos
    real_servos = [10,11]
    for servos in servo_angles:     
        i = 0
        for servo in servos:
            update_servo(servo,real_servos[i])
            i += 1
        time.sleep(timestep)
            


move_servos(tasks[0])