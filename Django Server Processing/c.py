import numpy as np
import scipy.ndimage as ndimage

import cv2
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
from mpl_toolkits.mplot3d import Axes3D


fullpath = "C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection/csp_app/2.jpg"
mat = imread(fullpath)  # reading image

mat = mat[:, :, 0]  # get the first channel
rows, cols = mat.shape  # getting shape present

xv, yv = np.meshgrid(range(cols), range(rows)[::1])  # forming grids

blurred = ndimage.gaussian_filter(mat, sigma=(5, 5), order=0)  # applying gaussian filter
fig = plt.figure(figsize=(6, 6))  # ploting image with size 6

ax = fig.add_subplot(221)  # displaying it
ax.imshow(mat, cmap='gray')  # displaying in grayscale

ax = fig.add_subplot(222, projection='3d')  # projecting to 3D
ax.elev = 80  # elevation angle =80

ax.plot_surface(xv, yv, mat, cmap='viridis')  # plotting 3D plot in viridis form

zmin, zmax = ax.get_zlim()  # min and max value of z
h = zmax - zmin  # max z-plot - min z-plot

depth = h * 0.00147 * 1616  # Formula Used: 1mm = 26pixel -> 1 Sq.pixel = 0.00147 (i.e 1/26*26)
finaldepth = depth / 100

# if (finaldepth < '3'):
#     print("Result: Less Risk Pothole")
# elif (finaldepth < '6'):
#     print("Result: Moderate Risk Pothole")
# else:
#     print("Result: High Risk Pothole")

print("The depth of the pothole is ", finaldepth, "cm")  # final depth

ax = fig.add_subplot(223)
ax.imshow(blurred, cmap='gray')

ax = fig.add_subplot(224, projection='3d')
ax.elev = 80

# Setting X, Y, Z
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# plotting 3D plot in viridis form
ax.plot_surface(xv, yv, blurred, cmap='viridis')

# displaing plot on screen
plt.show()
