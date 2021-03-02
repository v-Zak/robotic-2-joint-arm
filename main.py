import tkinter
import math

class segment:
    def __init__(self, canvas, target_position, a_position, angle, length):
        self.canvas = canvas
        self.target_position = target_position
        self.a_position = a_position
        self.angle = math.radians(angle)
        self.length = length
        self.b_position = position(0,0)
        self.calculate_b()
        self.line = canvas.create_line(self.a_position.x, self.a_position.y, self.b_position.x, self.b_position.y, fill = "white", width = 10)
           
    def update(self):
        direction = self.target_position.sub(self.a_position)
        self.angle = math.atan2(direction.y, direction.x)        
        direction.set_mag(self.length)
        direction.x *= -1
        direction.y *= -1
        self.a_position = self.target_position.add(direction)
        
    
    def calculate_b(self):
        self.b_position.x = self.a_position.x + self.length * math.cos(self.angle)
        self.b_position.y = self.a_position.y + self.length * math.sin(self.angle)
    
    def fix_to_base(self,distance_to_base):
        self.a_position = self.a_position.add(distance_to_base)
        
    def show(self):        
        self.canvas.coords(self.line, self.a_position.x, self.a_position.y, self.b_position.x, self.b_position.y)        

class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        dx = self.x + other.x
        dy = self.y + other.y
        ans = position(dx,dy)
        return ans
    
    def sub(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        ans = position(dx,dy)
        return ans

    def get_mag(self):
        ans = math.sqrt(self.x * self.x + self.y * self.y)
        return ans
    
    def set_mag(self, magnitude):
        current_magnitude = self.get_mag()
        new_magnitude = magnitude
        dmagnitude = new_magnitude/current_magnitude
        self.x *= dmagnitude
        self.y *= dmagnitude 

    def copy(self):
        ans = position(self.x, self.y)
        return ans
        

#1 pixel = 1mm for calculation purposes
height = 800
width = 800
number_of_segments = 2
segment_length = 75
arm = []
base_position = position(width/8,height/2)
framerate = 48 #fps
#timestep in ms based on framerate
timestep = int(1000*(1/framerate))
pressed = False
previous_end_pos = None

root = tkinter.Tk()
root.title("Robot Arm")    
canvas = tkinter.Canvas(root,bg="black", height=height, width=width)

initial_a_position = position(100,100)
mouse_pos = position(0,0)

target = mouse_pos
for i in range(number_of_segments):
    arm.append(segment(canvas,target, initial_a_position, 10, segment_length))
    target = arm[i].a_position

def main(): 
    global previous_end_pos
    mouse_x = root.winfo_pointerx() - root.winfo_rootx() 
    mouse_y = root.winfo_pointery() - root.winfo_rooty()
    mouse_pos = position(mouse_x, mouse_y)

    target = mouse_pos
    for segment in arm:
        segment.target_position = target
        segment.update()
        target = segment.a_position

    distance_to_base = base_position.sub(arm[-1].a_position)
    for segment in arm:
        segment.fix_to_base(distance_to_base)
        segment.calculate_b()
        segment.show()
    
    end_pos = arm[0].b_position    

    if pressed:       
        if previous_end_pos:
            canvas.create_line(previous_end_pos.x, previous_end_pos.y, end_pos.x, end_pos.y, fill = "red", width = 5)
                 
    previous_end_pos = end_pos.copy()
    canvas.after(timestep, main)

def key_pressed(event):
    global pressed
    pressed = True
    

def key_released(event):
    global pressed
    pressed = False





canvas.bind("<Button-1>", key_pressed)
canvas.bind("<ButtonRelease-1>", key_released)
canvas.pack()
main()
root.mainloop()