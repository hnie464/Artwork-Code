# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:27:26 2022

@author: Hendrik
"""

import matplotlib.pyplot as plt
import numpy as np
import tifffile as tf #install tiffle: pip install tiffile
import analysisFunctionsGallery as af

# Range of B-scan values you want processed...
start = 100
finish = 200   # 501 MAX for 392x500 B-scans

# 850nm Folders: (500,392)
#            'E:/Mini-Project/850nm system/front/area1/trial1/area1_t1.tif'         'E:/Mini-Project/850nm system/front/area1/trial2/area1_t2.tif'
#            'E:/Mini-Project/850nm system/front/area2/trial1/area2_t1.tif'         'E:/Mini-Project/850nm system/front/area3/trial1/area3_t1.tif'
#            'E:/Mini-Project/850nm system/front/area4/trial1/area4_t1.tif'


im = tf.imread(r'D:\Honours Project\Carlie Data\OCT\SWALT_002_220607_OCT\SWALT_002_Cscan_Crop.tif')   # Reads from .tif
x = np.arange(0,im.shape[2],1)

test_proj_top = []   # Creates an empty list to append arrays into
for i in range(start, finish + 1):
     x = x - start + 1;
     surf = af.surfaceDetect(im[i,0:im.shape[1],0:im.shape[2]],thresh=30000,padSize=0,scale=1,buffer=10,skip=5)   # For 392x500 B-scans
     test_proj_top.append(surf)   # Appends each array into list
     
plt.imshow(test_proj_top, cmap='gray')