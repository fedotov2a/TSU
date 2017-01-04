from Tkinter import *

coord_file    = open('coord.txt', 'r')
min_path_file = open('min_path.txt', 'r')

def create_point(x, y, r, color):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)

coord = []
for line in coord_file:
    coord.append(line[:-1].split(" "))

min_len_path = min_path_file.readline()
min_path = min_path_file.readline().split(" ")[:-1]

coord_file.close()
min_path_file.close()

root = Tk()
canvas = Canvas(root, width=600, height=600)

for i in range(len(min_path) - 1):
    x = int(coord[int(min_path[i])][0])
    y = int(coord[int(min_path[i])][1])
    x_next = int(coord[int(min_path[i+1])][0])
    y_next = int(coord[int(min_path[i+1])][1])

    create_point(x, y, 3, 'black' if i != 0 else 'blue')
    canvas.create_line(x, y, x_next, y_next, fill='red', width=1, arrow="last")
    canvas.create_text(x-10, y-10, anchor=W, font="Purisa", text=min_path[i])


canvas.pack()
root.mainloop()