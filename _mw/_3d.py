import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

file = open('sk_3d_points.txt', 'r')
x = []
y = []
z = []

for i, line in enumerate(file):
    if i % 10 == 0:
        x_, y_, z_ = line.split(' ')
        if float(z_) > 20:
            continue
        x.append(float(x_))
        y.append(float(y_))
        z.append(float(z_))
    # x, y, z = float(x), float(y), float(z)
    # ax.scatter(x, y, z, s = 1, c = 'green')

ax.plot_trisurf(x, y, z, cmap='jet')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

file.close()

plt.show()