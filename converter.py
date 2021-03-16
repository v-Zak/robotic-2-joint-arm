"41.269250430844856 71.82374207264324 | 42.980050940806315 72.99282382825892 |"

import time
import RPi.GPIO as GPIO

servo_pins = [17,22]

with open("output.txt","r") as r:
    tasks = r.readlines()

temp3 = [] 
number_of_tasks = 0
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
    number_of_tasks += 1
tasks = temp3
def get_pwm(angle):
    pwm = angle/18 + 2.5
    return pwm

class real_servo:
    def __init__(self,_servo_pin,start):
        self.servoPIN = _servo_pin
        GPIO.setup(self.servoPIN, GPIO.OUT)

        self.p = GPIO.PWM(self.servoPIN, 50)  #for PWM with 50Hz
        self.p.start(start)
        time.sleep(0.5) 
    
    def update(self,pwm):
        self.p.ChangeDutyCycle(pwm)

def update_servo(angle,real_servo):
    pwm = get_pwm(angle)
    real_servo.update(pwm)  


def move_servos(servo_angles, *args):
    try:
        real_servos = []
        timestep = 1/24
        if args:
            timestep = args[0]
        #only considering 2 servos
        GPIO.setmode(GPIO.BCM)
        i = 0
        for servo in servo_angles[0]:            
            r = real_servo(servo_pins[i],get_pwm(servo))
            real_servos.append(r)
            i+=1

        for servos in servo_angles:     
            i = 0
            for servo in servos:
                update_servo(servo,real_servos[i])
                i += 1
            time.sleep(timestep)
    
    finally:
        GPIO.cleanup()

print(f"The total number of tasks is {number_of_tasks}")               
answer = int(input("task number (1st = 1): "))
move_servos(tasks[answer-1])