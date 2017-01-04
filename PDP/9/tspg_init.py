from Tkinter import *
from math import sqrt

k = 0
root = Tk()
canvas = Canvas(root, width=600, height=600)
r = 3
coord_f = open('coord.txt', 'w')
coord = []


def create_point(event):
    global k
    canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill='black')
    canvas.create_text(event.x-10, event.y-10, anchor=W, font="Purisa", text=str(k))
    k += 1
    print >> coord_f, event.x, event.y
    coord.append([event.x, event.y])

def euclid_distance(p, q):
    return sqrt( (p[0] - q[0])**2 + (p[1] - q[1])**2 )

canvas.bind("<Button-1>", create_point)
canvas.pack()

root.mainloop()
coord_f.close()

matrix_distance = []
matrix_f = open('matrix_distances.txt', 'w')

for p in coord:
    for q in coord:
        matrix_distance.append(euclid_distance(p, q))

print >> matrix_f, len(coord)

for i in range(len(coord)):
    for j in range(len(coord)):
        print >> matrix_f, matrix_distance[i*len(coord) + j]
matrix_f.close()