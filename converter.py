"41.269250430844856 71.82374207264324 | 42.980050940806315 72.99282382825892 |"

with open("output.txt","r") as r:
    tasks = r.readlines()

temp2 = [] 
for task in tasks:  
    temp = []  
    task = task.split(" | ")
    task.pop(-1)
    for angles in task:
        angles = angles.split()
        for angle in angles:
            angle = float(angle)
        temp.append(angles)
    temp2.append(temp)
tasks = temp2