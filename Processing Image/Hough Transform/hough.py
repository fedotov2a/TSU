from matplotlib import cm
from skimage.transform import hough_line, hough_line_peaks
from skimage import data
from skimage import io

import numpy as np
import matplotlib.pyplot as plt

# img = io.imread('trih.bmp')
img = io.imread('starh.bmp')
image = np.zeros((img.shape[0], img.shape[1]))
for y in range(img.shape[1]):
    for x in range(img.shape[0]):
        if img[x][y][0] == 255:
            image[x][y] = 255

h, theta, d = hough_line(image)

fig, (ax0, ax1, ax2) = plt.subplots(1, 3)
plt.tight_layout()

ax0.imshow(image, cmap=cm.gray)
ax0.set_title('Input image')
ax0.set_axis_off()

ax1.imshow(np.log(1 + h), extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]], cmap=cm.gray, aspect=1/1.5)
ax1.set_title('Hough transform')
ax1.set_xlabel('Angles (degrees)')
ax1.set_ylabel('Distance (pixels)')
ax1.axis('image')
ax1.set_axis_off()

ax2.imshow(image, cmap=cm.gray)
row1, col1 = image.shape
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    # y0 = int((dist -    0 * np.cos(angle)) / np.sin(angle))
    # y1 = int((dist - col1 * np.cos(angle)) / np.sin(angle))
    # print("---------------------")
    y = []
    p0 = (0, 0)
    p1 = (0, 0)
    first_point = True
    for x in range(col1):
        yy = int(round((dist - x*np.cos(angle)) / np.sin(angle)))
        if first_point:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if x+j < col1 and yy + i < row1 and x+j >= 0 and yy + i >= 0 and image[yy+i][x+j] == 255:
                        p0 = (x+j, yy+i)
                        first_point = False
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if x+j < col1 and yy + i < row1 and x+j >= 0 and yy + i >= 0 and image[yy+i][x+j] == 255:
                        p1 = (x+j, yy+i)
        y.append(yy)

    ax2.plot([x for x in range(col1)], y, '-g', linewidth=1)
    if p0[0] != 0 and p0[1] != 0 and p1[0] != 0 and p1[1] != 0:
        ax2.plot((p0[0], p1[0]), (p0[1], p1[1]), '-r', linewidth=2)
    
    x_wp = p0[0]
    y_wp = p1[0]
    for x in range(p0[0]+1, p1[0]+1):
        yy = int(round((dist - x*np.cos(angle)) / np.sin(angle)))
        wp = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+j < col1 and yy + i < row1 and x+j >= 0 and yy + i >= 0 and image[yy+i][x+j] == 255:
                    x_wp = x + j
                    y_wp = yy + i
                    wp = True
                    break
            if wp:
                break

        if not wp:
            if np.sqrt((x - x_wp)**2 + (yy - y_wp)**2) >= 45:
                ax2.plot((x_wp, x), (y_wp, yy), '-k', linewidth=3)

    # удаление линий внутри фигур типа "звезда"
    fp = True
    for x in range(min(p0[0], p1[0]), max(p0[0], p1[0])):
        y_x = int(round((dist - x*np.cos(angle)) / np.sin(angle)))
        if fp:
            xx = x
            yy = y_x
            fp = False
            continue

        wh_p = False
        for i in range(-2, 3):
            for j in range(-2, 3):
                if image[y_x+i][x+j] == 255 and y_x + i != yy and x + j != xx:
                    xx, yy = x+j, y_x+i
                    wh_p = True
                    break
            if wh_p:
                break

        if wh_p:
            if np.sqrt((x - xx)**2 + (y_x - yy)**2) <= 10:
                ax2.plot((xx, x), (yy, y_x), '-r', linewidth=3)
   
            xx = x
            yy = y_x

    ax2.plot((0, col1), (y0, y1), '-r', linewidth=2)
    ax2.plot((p0[0], p1[0]), (p0[1], p1[1]), '-r', linewidth=3)

ax2.axis((0, col1, row1, 0))
ax2.set_title('Detected lines')
ax2.set_axis_off()

plt.show()
