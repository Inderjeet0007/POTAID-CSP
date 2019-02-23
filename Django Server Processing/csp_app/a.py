
import numpy as np
import cv2

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#Load the Image
fullpath = "C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection/csp_app/2.jpg"
imgo = cv2.imread(fullpath)
height, width = imgo.shape[:2]

#Create a mask holder
mask = np.zeros(imgo.shape[:2],np.uint8)

#Grab Cut the object
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

#Hard Coding the Rect… The object must lie within this rect.
rect = (10,10,width-30,height-30)
cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img1 = imgo*mask[:,:,np.newaxis]

#Get the background
background = imgo-img1

#Change all pixels in the background that are not black to white
background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

#Add the background and the image
final = background + img1

#To be done – Smoothening the edges….
# convert the image to grayscale
gray_image = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# convert the grayscale image to binary image
ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
x, y = thresh.shape
arr = np.zeros((x, y, 3), np.uint8)
# find contours in the binary image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    i= 0
    if cv2.contourArea(c) > 3000:
        i=i+1
        # calculate moments for each contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        # calculate x,y coordinate of center
        cv2.circle(final, (cX, cY), 5, (255, 255, 255), -1)
        cv2.fillConvexPoly(arr, c, [255, 255, 255])
        cv2.putText(final, 'Centroid', (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # print(cv2.arcLength(c, True)) # ARC LENGTH
        # print(cv2.contourArea(c)) # Unit is pixel
        #Formula Used: 1mm = 26pixel -> Area 1 Sq.pixel = 0.00147 (i.e 1/26*26)
        # Therefore the area would be no of pixel * Area of 1 sq.pixel * 1616
        area_mm = round(0.00147 * cv2.contourArea(c) * 1616) #convert to mm^2
        area = area_mm/100 #convert to cm^2
        print(cv2.contourArea(c),'pixels')
        print('Area of the Pothole',i, 'is ',area,'square cm')

#showing image with foreground objects
cv2.imshow('image', final )
cv2.imwrite('area.jpg',final)

k = cv2.waitKey(0)

if k==27:
    cv2.destroyAllWindows()