# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:24:38 2020

@authors: mbro632 & hnie464
"""

import os,sys

import matplotlib.pyplot as plt
import numpy as np
import time
import DirectorySetupGallery as directory
import TdmsCodeGallery as pytdms #Install npTDMS pip install npTDMS
import scipy as sci
from scipy import signal,ndimage
import pandas as pd
import glob
import tifffile as tf #install tiffle: pip install tiffile
import scipy as sci
import analysisFunctionsGallery as af
import cv2
import math
import PIL 
from PIL import Image

plt.close('all')

tstart=time.time()
#Data location information  
folderLocation = r'E:\Mini-Project\Artwork\G3'  
# Other Folders:   E:\Mini-Project\Artwork\G2,   E:\Mini-Project\Artwork\G3,   F:\2021\Art Gallery\G4,   F:\2021\Art Gallery\G5                                          
npy = r'\npy_files'                                                             
output = r'\output_files'                                                        

#PS-OCT Image information - These values never change
spectra_num = 1024
A_scan_num = 714
padSize = 0 #How much zero padding do you want to do

B_scan_num = 220 #default but may change on file

dataLocation = folderLocation
print(dataLocation)
sampleName = os.path.basename(dataLocation)
imageFiles1 = sorted(glob.glob(dataLocation + '/' + 'Ch0_G*.tdms'))
imageFiles  = sorted(glob.glob(dataLocation + '/' + 'Ch1_G*.tdms'))


imageSize = np.array(())
stackedImages = np.array(())
for images in imageFiles:
    print(images)
    B_scan_num = int(images.split('_')[2]) #How many B-scans were in the volume image
    variableName = images.split('/')[-1].split('_',1)[-1].rsplit('.',1)[0] #get the XXXXXX filename details after Ch1_XXXXXXX.tdms
    Int = []
    Ret = []
    Ch0Complex = []
    Ch1Complex = []
    t1 = time.time()
    Int,Ret = directory.loadData(dataLocation,npy,output,variableName,A_scan_num,B_scan_num,padSize)    #Load the  
    intdB = 10*np.log10(Int) #put in log scale
    intdB[:,0:5,:] = 70 #Remove artifact noise values at the start of the array (noise level is ~70)
    
    imageSize = np.append(imageSize, B_scan_num)
    
    # plt.figure()
    # plt.imshow(intdB[35,:,:],cmap='gray') # first element determines displayed B-scan
    # plt.ylim(250)
    # #plt.axis('off')
    
    plt.figure()
    abd = cv2.flip(intdB[35,:,:], 1)
    plt.imshow(abd,cmap='gray') # first element determines displayed B-scan
    plt.ylim(250)
    #plt.axis('off')

    #Save tiff image - Can be used in ImageJ later.
    tf.imwrite(folderLocation + output + '/' + variableName + '/Int_{}.tif'.format(variableName.split('_')[2]) ,intdB.astype(np.float32),photometric='minisblack')
    
    # FOR ROTATING B-SCAN DIRECTION
    #tf.imwrite(folderLocation + output + '/' + variableName + '/Int_flip{}.tif'.format(variableName.split('_')[2]) ,np.transpose(intdB.astype(np.float32)),photometric='minisblack')
    stackedImages = np.append(stackedImages, intdB)
    
    
finalImage = stackedImages.reshape(int(np.sum(imageSize)),int(spectra_num/2),np.size(intdB,2))


# PROJECTION VIEW

projection = np.sum(finalImage[:,10:250,:],1)
#projection = cv2.flip(projection, 1)   # For G5 to flip
#projection = np.rot90(projection, 2)   # For G3 to rotate
plt.figure()
plt.imshow(projection, cmap='gray',clim = [1.6e4,1.75e4])

# B-SCAN IMAGE FROM PERPENDICULAR DIRECTION
# B1Way = finalImage[:,:,1] #slice on one axis - line 300
# plt.figure()
# plt.imshow(np.rot90(B1Way,3),cmap='gray',clim=[70,110])
# plt.ylim(250)



# ~ FOR G2 (SECTION FLIP) ~
# a = projection[0:216]
# b = projection[217:460]
# test_image = np.vstack((b, a))
# plt.imshow(test_image, cmap='gray',clim = [1.6e4,1.75e4])



# ===================== ~ IRREGULARITY DETECTION ~ ===========================

plt.rc('figure', max_open_warning = 0)   # removes 20 plot limit warning


im = tf.imread('F:/2021/Art Gallery/G5/output_files/G5_220_(2)0_00/Int_(2)0.tif')   # Reads from .tif file
# FOLDERS:   'E:\Mini-Project\Artwork\G2\output_files\G2_240_(2)0_00\Int_(2)0.tif'   'E:\Mini-Project\Artwork\G2\output_files\G2_220_02_00\Int_02.tif'
#            'E:\Mini-Project\Artwork\G3\output_files\G3_220_(2)0_00\Int_(2)0.tif'   'E:\Mini-Project\Artwork\G3\output_files\G3_220_02_00\Int_02.tif'
#            'F:/2021/Art Gallery/G5/output_files/G5_220_(2)0_00/Int_(2)0.tif'      'F:/2021/Art Gallery/G5/output_files/G5_220_02_00/Int_02.tif'
#            'F:/2021/Art Gallery/G4/output_files/G4_220_(2)0_00/Int_(2)0.tif'      'F:/2021/Art Gallery/G4/output_files/G4_220_02_00/Int_02.tif'


# Range of B-scan values you want processed...
start = 0
finish = 219   # 219 Max


detected = False
x = np.arange(0,680,1)   # 680x512 B-scans
#x = np.arange(0,220,1)   # 220x512 B-scans


print('Processing...')

# ========================= PROJECTION MAPPING ===============================

count = 0
for i in range(start, finish + 1):   # +1 to include the end of the range in the list
    x = x - start + 1;   # make x start at 1
    surf = af.surfaceDetect(im[i,0:512,0:680],thresh=100,padSize=0,scale=1,buffer=10,skip=5)   # 680x512 B-scans
    #surf = af.surfaceDetect(im[i,0:680,0:512],thresh=100,padSize=0,scale=1,buffer=10,skip=5)   # 220x512 B-scans
    d_surf=[(surf[u+1]-surf[u]) for u in range(len(surf)-1)]   # localised change
    plt.imshow(projection[220:440], cmap='gray')   # projection[0:220] for top-half '(2)0', projection[220:440] for bottom-half '02'
    plt.ylim(220)   # limits the projection image to what is scanned
    plt.title('Projection with Irregularities Mapped')
    
    for m in d_surf:
        if m >= 2 in d_surf[20:660]:   # gradient threshold (..., -1, -2, 0, 1, 2, ...)
            detected = True
            max_value = max(d_surf)
            max_index = d_surf.index(max_value)
            count = count+1
            if max_index in np.arange(20,660):   # ignores start and end noise
                plt.plot(max_index, i, marker='+', color='lightgreen')
                break
        elif m <= -2 in d_surf[20:660]:
            detected = True
            max_value = max(d_surf)
            max_index = d_surf.index(max_value)
            count = count+1
            if max_index in np.arange(20,660):
                plt.plot(max_index, i, marker='+', color='lightgreen')
                break

# ========================== B-SCAN MAPPING ==================================

for n in range(start, finish + 1): 
    x = x - start + 1;
    surf = af.surfaceDetect(im[n,0:512,0:680],thresh=100,padSize=0,scale=1,buffer=10,skip=5)   # 680x512 B-scans
    #surf = af.surfaceDetect(im[n,0:680,0:512],thresh=100,padSize=0,scale=1,buffer=10,skip=5)   # 220x512 B-scans
    plt.figure()
    plt.ylim(250)
    plt.imshow(im[n,:,:],cmap='gray')
    x = np.arange(0,680,1)   # fixes issue where plot goes over 700 on x-axis
    line = plt.plot(x,surf,'-', color='red', linewidth=0.5)
    plt.title('B-Scan: n, '+ str(n))

    d_surf=[(surf[i+1]-surf[i]) for i in range(len(surf)-1)]   # localised change
    #print(d_surf)
    
    for m in d_surf:
        if m >= 2 in d_surf[20:660]:   # gradient threshold (..., -1, -2, 0, 1, 2, ...)
            detected = True
            max_value = max(d_surf)
            max_index = d_surf.index(max_value)
            if max_index in np.arange(20,660):   # ignores start and end noise
                plt.plot(x[max_index], surf[max_index], marker='+', color='lightgreen')
                print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[max_index], 'y =', surf[max_index])
                break
        elif m <= -2 in d_surf[20:660]:
            detected = True
            max_value = max(d_surf)
            max_index = d_surf.index(max_value)
            if max_index in np.arange(20,660):
                plt.plot(x[max_index], surf[max_index], marker='+', color='lightgreen')
                print('Possible point of interest detected!   B-scan #', n, '   Location:', 'x =', x[max_index], 'y =', surf[max_index])
                break

# ============================= ALWAYS HAVE ON ===============================

print('Done!')
print('')

if detected == True:
    print('Irregularities Detected:', count)

if detected == False:
    print('Nothing of interest within the scanning range:', start, '-', finish)
