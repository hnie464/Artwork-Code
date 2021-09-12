#Analysis Functions
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal,ndimage
import scipy as sci
import cv2
import time


    
def surfaceDetect(intdB,thresh,padSize,scale,buffer,skip):
    kernel = np.ones((5,5),np.uint8)
    intdB = sci.ndimage.median_filter(intdB, size=(7,7))
    length = np.size(intdB,1)
    surfaceTemp =np.zeros(length)
    start = 5
    buffer = 4   # 20
    skip = -2   # 0
    for i in range(0,length):
        count = 0
        for j in range(start,len(intdB[:,int(i)])):
            if intdB[j,int(i)]>thresh:
                count += 1
            else:
                count = 0
            if count == buffer:
                surfaceTemp[i] = j - buffer + skip
                #maxPos = np.max(1)
                #if surfaceTemp[i]
                break
     
#Now we want to go through a correction loop and find any locations that have no surface identified and slowly lower the requirements
    x= np.where(surfaceTemp==0)[0]

    for i in enumerate(x):
        threshNew = thresh
        count = 0
        done = False
        bufferNew = int(buffer/2)
        while done == False:
            threshNew = threshNew - 1
            #print('threshold is now {}'.format(threshNew))
            for j in range(start,len(intdB[:,int(i[1])])):
                if intdB[j,int(i[1])]>threshNew:
                    count += 1
                else:
                    count = 0
                if count == bufferNew:
                    surfaceTemp[i[1]] = j - bufferNew + skip
                    done = True
                    #print('new surface value found')
                    break
        
    if int((len(surfaceTemp)/35)//2*2+1)<3:   # /35 for standard
        windowLength=3   # 3
    else:
        windowLength = int((len(surfaceTemp)/55)//2*2+1)    # /55 for standard
    surface= signal.savgol_filter(surfaceTemp, windowLength,2).astype(int)
    #surface[surface<4] = 5
    #y= np.where(surface<0)[0]
    #for i in y:
    #    surface[i] = surfaceTemp[i]
    # = surfaceTemp.astype(int)    
    return(surface)

def dilateErode(intdB, kernel):
    intDil = cv2.dilate(intdB,kernel,iterations=2)
    intErosPost = cv2.erode(intDil,kernel,iterations=3)
    intErosPost = sci.ndimage.median_filter(intErosPost, size=(7,7))
    return(intErosPost)
    
def depthDetectBscan(intdB,thresh,padSize,scale, surface, buffer,skip):    
    #intdB = 10*np.log(intensity)
    #kernel = np.ones((5,5),np.uint8)
    #intdB = dilateErode(intdB, kernel)
    intdB= ndimage.filters.gaussian_filter(intdB,9*int(scale),0)
    #plt.figure()
    #plt.imshow(intdB,cmap='binary')
    #plt.clim([170,200])
    #plt.figure()
    #plt.plot(intdB[:,350])
    depthFinal = np.ones((np.size(surface,0)))
    count = 0
    for i in range(0,len(surface)):
        for j in range(surface[i],len(intdB)):
            if intdB[j,i]<thresh:
                count +=1
            else:
                count =0
            if count == buffer:
                depth = j - buffer + skip
                depthFinal[i] = depth
                break
            if j == len(intdB)-1:
                depth  = j - 100
                depthFinal[i] = depth
    return(depthFinal)    
    
def depthDetect(intdB,thresh,padSize,scale, surface, buffer,skip):    
    #intdB = 10*np.log(intensity)
    #kernel = np.ones((5,5),np.uint8)
    #intdB = dilateErode(intdB, kernel)
    intdB= ndimage.filters.gaussian_filter(intdB,9*int(scale),0)
    #plt.figure()
    #plt.imshow(intdB,cmap='binary')
    #plt.clim([170,200])
    #plt.figure()
    #plt.plot(intdB[:,350])
    count = 0
    for j in range(surface,len(intdB)):
        if intdB[j]<thresh:
            count +=1
        else:
            count =0
        if count == buffer:
            depth = j - buffer + skip
            break
        if j == len(intdB)-1:
            depth  = j - 100
    return(depth)


    


    
def surfaceIrregularity(surface, smoothVal):
    surfaceFit = signal.savgol_filter(surface, smoothVal,2).astype(int)
    diff = surface - surfaceFit
    irregularity = np.std(diff)
    return(surfaceFit,irregularity)    


