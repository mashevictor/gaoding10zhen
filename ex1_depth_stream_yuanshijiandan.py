#!/usr/bin/env python
from skimage import io,transform,data
import matplotlib.pyplot as plt
import numpy as np
import cv2
np.set_printoptions(threshold=np.inf)
from primesense import openni2
from primesense import _openni2 as c_api
dist ='/home/victor/software/OpenNI-Linux-x64-2.3/Redist'
openni2.initialize(dist)
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320, resolutionY=240, fps=30))
depth_stream.set_mirroring_enabled(False)
depth_stream.start()

def get_depth():
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240,320)
    #dmap=transform.resize(dmap, (120,160))
    print(dmap.dtype)
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1)
    d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    print(d4d.dtype)
    d4d = 255 - d4d    
    return dmap, d4d
s=0
done = False
while not done:
    key = cv2.waitKey(1)
    key = cv2.waitKey(1) & 255
    if key == 27:
        print "\tESC key detected!"
        done = True
    elif chr(key) =='s':
        print "\ts key detected. Saving image and distance map {}".format(s)
        cv2.imwrite("ex1_"+str(s)+'.png', d4d)
        np.savetxt("ex1dmap_"+str(s)+'.out',dmap)
    dmap,d4d = get_depth()
    print (dmap)
    cv2.imshow('depth', d4d)
cv2.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
