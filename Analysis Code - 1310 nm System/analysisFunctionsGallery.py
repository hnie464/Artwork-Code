#Analysis Functions
import numpy as np
#import matplotlib.pyplot as plt
from scipy import signal,ndimage
import scipy as sci
import cv2
import time


# Strict Surface Line (Red)
def surfaceDetect(intdB, thresh, buffer, skip):
    intdB = sci.ndimage.median_filter(intdB, size=(7, 7))
    length = np.size(intdB, 1)
    surfaceTemp = np.zeros(length)
    start = 5
    buffer = 10   # To reduce run times, set buffer to 1 (may cause spikes along surface).
    skip = 0
    for i in range(0,length):
        count = 0
        for j in range(start, image[:, 0].size):
            if intdB[j,int(i)] > thresh:
                count += 1
            else:
                count = 0
            if count == buffer:
                surfaceTemp[i] = j - buffer + skip
                break
     
#Now we want to go through a correction loop and find any locations that have no surface identified and slowly lower the requirements
    x= np.where(surfaceTemp==0)[0]

    for i in enumerate(x):
        threshNew = thresh
        count = 0
        done = False
        bufferNew = int(buffer/2)
        while done == False:
            threshNew = threshNew - (thresh/100)
            #print('threshold is now {}'.format(threshNew))
            for j in range(start, image[:, 0].size):
                if intdB[j,int(i[1])] > threshNew:
                    count += 1
                else:
                    count = 0
                if count == bufferNew:
                    surfaceTemp[i[1]] = j - bufferNew + skip
                    done = True
                    #print('new surface value found')
                    break
        
    windowLength = 3    # (Higher value = Smoother surface line)
    surface= signal.savgol_filter(surfaceTemp, windowLength,2).astype(int)   
    return(surface)


# Smooth Surface Line (Blue)
def surfaceDetect2(intdB, thresh, buffer, skip):
    intdB = sci.ndimage.median_filter(intdB, size=(7, 7))
    length = np.size(intdB, 1)
    surfaceTemp = np.zeros(length)
    start = 5
    buffer = 10
    skip = 0
    for i in range(0, length):
        count = 0
        for j in range(start, image[:, 0].size):
            if intdB[j,int(i)] > thresh:
                count += 1
            else:
                count = 0
            if count == buffer:
                surfaceTemp[i] = j - buffer + skip
                break
     
#Now we want to go through a correction loop and find any locations that have no surface identified and slowly lower the requirements
    x= np.where(surfaceTemp==0)[0]

    for i in enumerate(x):
        threshNew = thresh
        count = 0
        done = False
        bufferNew = int(buffer/2)
        while done == False:
            threshNew = threshNew - (thresh/100)
            #print('threshold is now {}'.format(threshNew))
            for j in range(start, image[:, 0].size):
                if intdB[j,int(i[1])] > threshNew:
                    count += 1
                else:
                    count = 0
                if count == bufferNew:
                    surfaceTemp[i[1]] = j - bufferNew + skip
                    done = True
                    #print('new surface value found')
                    break
        
    windowLength = 31    # (Higher value = Smoother surface line)
    surface= signal.savgol_filter(surfaceTemp, windowLength,2).astype(int)  
    return(surface)
