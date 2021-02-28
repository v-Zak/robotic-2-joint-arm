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
        


height = 400
width = 400
base_position = position(50,200)
framerate = 48 #fps
#timestep in ms based on framerate
timestep = int(1000*(1/framerate))

root = tkinter.Tk()
root.title("Robot Arm")    
canvas = tkinter.Canvas(root,bg="black", height=height, width=width)       
canvas.pack()

initial_a_position = position(100,100)
mouse_pos = position(0,0)
segment1 = segment(canvas ,mouse_pos, initial_a_position, 10, 100)
segment2 = segment(canvas ,segment1.a_position, initial_a_position, 10, 100)

def main():   
    mouse_x = root.winfo_pointerx() - root.winfo_rootx() 
    mouse_y = root.winfo_pointery() - root.winfo_rooty()
    mouse_pos = position(mouse_x, mouse_y)

    segment1.target_position = mouse_pos    
    segment1.update()   

    segment2.target_position = segment1.a_position    
    segment2.update() 

    distance_to_base = base_position.sub(segment2.a_position)

    segment1.fix_to_base(distance_to_base)
    segment2.fix_to_base(distance_to_base)  

    segment1.calculate_b()
    segment2.calculate_b()

    segment1.show()
    segment2.show()

    canvas.after(timestep, main)

main()

root.mainloop()