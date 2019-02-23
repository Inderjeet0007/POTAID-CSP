# import the necessary packages

from scipy.spatial import distance as dist
import requests
import cv2
import numpy as np


# define the URL to our face detection API
url = "http://127.0.0.1:8000/face_detection/detect/"


# use our detection API to find potholes in images via image URL
def pothole(img_path, id):
    fullpath="C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection"+img_path
    image = cv2.imread(fullpath)


    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(frame,(7,7),1)
    median = cv2.medianBlur(blur,9)
    dilate = cv2.dilate(median, None, iterations=2)
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    erode = cv2.dilate(opening, None, iterations=1)
    edges = cv2.Canny(erode,80,160)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours = imutils.grab_contours(contours)
    # c = max(contours,key=cv2.contourArea)
    # focalLength = (c[1][0] * 24.0)/11.0


    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 40

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.08


    # Detect the blobs in the image
    if cv2.__version__.startswith('2.'):
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    # Draw detected keypoints as blue circles
    keypoints = detector.detect(erode)
    print("Total No of potholes are:")
    print(len(keypoints))
    print(keypoints)

    if (len(keypoints)>=1):
        print("Pothole Found")
    else:
        print("No Pothole Found")

    # Get Heatmap
    frame = cv2.applyColorMap(erode, cv2.COLORMAP_HSV)
    # cv2.drawContours(frame, contours, -1, (94,206,165), 2)
    cv2.drawContours(frame, contours, -1, (255,0,149), 2)


    # Get the moments
    mu = [None]*len(contours)
    for i in range(len(contours)):
        mu[i] = cv2.moments(contours[i])

    # Get Area, Length, ARC Length
    for i in range(len(contours)):
            print(' * Contour[%d] - Area (M_00) = %.2f - Area OpenCV: %.2f - Length: %.2f' % (i, mu[i]['m00'], cv2.contourArea(contours[i]), cv2.arcLength(contours[i], True)))
            # ellipse = cv2.fitEllipse(contours[i])
            # cv2.ellipse(frame, ellipse, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Pothole_Image_v", frame)
    cv2.imshow("Org_Image_v", image)
    cv2.imwrite("processed.jpg", frame)
    cv2.imwrite("original.jpg", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
