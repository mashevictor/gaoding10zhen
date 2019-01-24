#!/usr/bin/env python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
import cv2
from primesense import openni2
from primesense import _openni2 as c_api
dist ='/home/victor/software/OpenNI-Linux-x64-2.3/Redist'
openni2.initialize(dist)
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"
dev = openni2.Device.open_any()
rgb_stream = dev.create_color_stream()
print 'The rgb video mode is', rgb_stream.get_video_mode() 
rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=15))
rgb_stream.start()
rgb_stream.set_mirroring_enabled(False)
def get_rgb():
    bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(240,320,3)
    rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
    return rgb    
s=0
done=False
rgbs=[]
c=1
timeF=10
while not done:
    key = cv2.waitKey(1) & 255
    if key == 27:
        break
    elif chr(key) =='s':
        print "\ts key detected. Saving image {}".format(s)
        cv2.imwrite("ex2_"+str(s)+'.jpg', rgb)
    rgb = get_rgb()
    cv2.imshow('rgb', rgb)
    if(c%timeF==0):
        cv2.imwrite('image/'+str(c) + '.jpg',rgb)
    	cv2.imshow('rgb10', rgb)
    c=c+1
cv2.destroyAllWindows()
rgb_stream.stop()
openni2.unload()
print ("Terminated")
