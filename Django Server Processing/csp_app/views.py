from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import numpy as np
import urllib
import json
import cv2
import os
import base64
import requests
import subprocess
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from csp_app.BaseResponseEntity import BaseResponseEntity, ComplexEncoder
from csp_app.serializers import ImageSerializer
from csp_app.test_api import pothole
# from csp_app.test import depth
# from csp_app.c import area
from .forms import ImageForm, UpdateImage
from .models import Image

# Create your views here.
# define the path to the face detector
# FACE_DETECTOR_PATH = "C:/Users/Inderjeet Saluja/Documents/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"


@csrf_exempt
def image_view(request):
    # if request.method == 'POST':
    #     form = ImageForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('success')
    # else:
    #     form = ImageForm()
    # return render(request, 'home.html', {'form': form})
    Data = {}
    lResponse = BaseResponseEntity()
    try:

        # getting data from android app
        imagefile = request.POST.get('imagefile')
        print(imagefile)
        lat = request.POST.get('lat')
        long = request.POST.get('long')

        #saving the data in the database
        lUserD = Image()
        lUserD.imagefile = imagefile
        lUserD.lat = lat
        lUserD.long = long
        lUserD.save()

        Data['Message'] = 'Data Inserted Successfully.'
        Data['Responsecode'] = 200

        # lResponse.ResponseCode = 200
        lResponse = Data

        data = json.dumps(lResponse, cls=ComplexEncoder)

        save_path = 'C:/Users/Inderjeet Saluja/Desktop/projects/pothole_detection/media/images'
        name_of_file = 'image_decode'
        completeName = os.path.join(save_path, name_of_file+".png")


        imagedata = base64.b64decode(imagefile)
        # filename = 'image_decode.png'
        with open(os.path.join(completeName), "wb") as f:
            f.write(imagedata)
            f.close()

        return HttpResponse(data, content_type='application/json', status=200)
    except Exception as e:
        print(e)
        # lResponse.ResponseCode = 500
        Data['responsecode'] = 500
        lResponse = Data

        data = json.dumps(lResponse, cls=ComplexEncoder)
        return HttpResponse(data, content_type='application/json', status=500)

@csrf_exempt
def api_get_latlong(request):
    latLong = []
    lResponse = BaseResponseEntity()
    try:
        lImage = Image.objects.all()
        for singleRecord in lImage:
            my_dict = {}
            my_dict['lat'] = singleRecord.lat
            my_dict['long'] = singleRecord.long
            latLong.append(my_dict)

        print(latLong)
        lResponse.Data = latLong
        lResponse.ResponseCode = 200

        data = json.dumps(lResponse.toJSONData(), cls=ComplexEncoder)
        print(data)
        return HttpResponse(data, content_type='application/json', status=200)
    except Exception as e:
        print(e)
        return HttpResponse(content_type='application/json', status=500)

def update_view(request):
    obj = Image.objects

    if request.method == 'POST':
        form = UpdateImage(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UpdateImage()
    return render(request, 'update.html', {'form': form, 'obj': obj})


def success(request):
    return HttpResponse('successfuly uploaded')


def processing_images(request):
    if request.method == 'GET':
        #getting the latest created_at field data
        # obj = Image.objects.latest('created_at')
        # print(obj.imagefile.url)
        obj ='C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/media/images/2.jpg'
        # finding pothole occurance
        # pothole(obj.imagefile.url, obj.id)
        cmd = 'C:/Users/"Inderjeet Saluja"/Documents/env/Scripts/python C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/predict.py -c C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/config.json -w C:/Users/"Inderjeet Saluja"/Desktop/projects/pothole_detection/csp_app/potholes-detection-master/trained_wts.h5 -i ' + obj
        # execute the cmd command
        os.system(cmd)

        # finding area
        # area(obj)
        #
        # #finding depth
        # depth(obj)

        return render(request, 'process.html', {'object': obj})


@csrf_exempt
def detect(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":

        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])

        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get("url", None)

            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)

            # load the image and convert
            image = _grab_image(url=url)

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
        rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

        # update the data dictionary with the faces detected
        data.update({"num_faces": len(rects), "faces": rects, "success": True})

    # return a JSON response
    return JsonResponse(data)


# def _grab_image(path=None, stream=None, url=None):
#     # if the path is not None, then load the image from disk
#     if path is not None:
#         image = cv2.imread(path)
#
#     # otherwise, the image does not reside on disk
#     else:
#         # if the URL is not None, then download the image
#         if url is not None:
#             resp = urllib.request.urlopen(url)
#             data = resp.read()
#
#         # if the stream is not None, then the image has been uploaded
#         elif stream is not None:
#             data = stream.read()
#
#         # convert the image to a NumPy array and then read it into
#         # OpenCV format
#         image = np.asarray(bytearray(data), dtype="uint8")
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#     # return the image
#     return image
