# import numpy as np
# import scipy.ndimage as ndimage
#
#
# import cv2
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import imread
# from mpl_toolkits.mplot3d import Axes3D
#
# fullpath="C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection/csp_app/area.jpg"
# mat = imread(fullpath)
# # imageFile = 'C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection/csp_app/cannycheck4.jpg'
# # mat = imread(imageFile)
# mat = mat[:, :, 0]  # get the first channel
# rows, cols = mat.shape
# xv, yv = np.meshgrid(range(cols), range(rows)[::1])
#
# blurred = ndimage.gaussian_filter(mat, sigma=(5, 5), order=0)
# fig = plt.figure(figsize=(6, 6))
#
# ax = fig.add_subplot(221)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
#
#
# #blur image output
# ax.imshow(mat, cmap='gray')
#
# ax = fig.add_subplot(222, projection='3d')
# ax.set_zlim(0,500)
# ax.elev = 80
# ax.plot_surface(xv, yv, mat, cmap='viridis')
#
# ax = fig.add_subplot(223)
# ax.imshow(blurred, cmap='gray')
#
# ax = fig.add_subplot(224, projection='3d')
# ax.elev = 8
#
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.plot_surface(xv, yv, blurred, cmap='viridis')
# ymin, ymax = ax.get_zlim()
# plt.show()
# print(ymax)
# print(ymin)
# import matplotlib.image as mpimg
# import numpy as np
# img = mpimg.imread(fullpath)
# lum_img = img[:, :, 0]
# imgplot = plt.imshow(lum_img)
# imgplot.set_cmap('nipy_spectral')
# plt.colorbar()
# plt.show()

import os

cmd ='C:/Users/"Inderjeet Saluja"/Documents/env/Scripts/python C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/predict.py -c C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/config.json -w C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/trained_wts.h5 -i C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/images/4.jpg'
        # print(cmd)
os.system(cmd)