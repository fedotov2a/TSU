import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2)

f = open('input.txt', 'r')
number_points = f.readline()

for line in f:
    coord = line.split(" ")
    ax[0].plot(coord[0], coord[1], 'bo')

f2 = open('output.txt', 'r')
number_centroids = f2.readline()

color   = ['ro', 'bo', 'co', 'mo', 'yo', 'ko', 'go']
color_c = ['r^', 'b^', 'c^', 'm^', 'y^', 'k^', 'g^']
k = 0
for line in f2:
    if k < int(number_centroids):
        centroid = line.split(" ")
        ax[1].plot(centroid[0], centroid[1], color_c[int(centroid[2].split('\n')[0])])
        k += 1
    else:
        point = line.split(" ")
        ax[1].plot(point[0], point[1], color[int(point[2].split('\n')[0])])

plt.show()
f.close()
f2.close()