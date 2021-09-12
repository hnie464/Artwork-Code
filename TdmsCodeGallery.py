# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:38:25 2019

@author: mbro632
"""
##Test
from nptdms import TdmsFile,TdmsWriter,ChannelObject,TdmsGroup,TdmsChannel
import matplotlib.pylab as plt
import numpy as np
from PIL import Image

### This module contains a collections of functions to read and process PS_OCT data

### Example of use:

### Read the raw data and convert to C_Scan matrix using the read_tdms function. The number of B_scans and A_scans are required to shape the C_scan:

#A_scan_num = 714
#B_scan_num = 150

#Data0  =  pytdms.read_tdms("Raw_C-Scan/G0_S1_XY_Ch0.tdms", A_scan_num, B_scan_num)
#Data1  =  pytdms.read_tdms("Raw_C-Scan/G0_S1_XY_Ch1.tdms", A_scan_num, B_scan_num)

###  Process the raw PS_OCT data to find the intensity and retardation matrices using the Scan_processing_3D function. If save == True the processed data will be saved as a numpy arrays with the given name.

#Int, Ret = pytdms.Scan_processing_3D(Data0,Data1,'Raw_C-Scan/G0_S1_XY',save = True)

### If you just want to process a single B_Scan you can use the Scan_processing_2D function. 

#Int_2D, Ret_2D = pytdms.Scan_processing_2D(Data0[50,:,:],Data1[50,:,:])

### to save the C_scan or B_scan as a tiff you can use the Save_Image funtion:

## to save a C_Scan:
#pytdms.Save_Image('Raw_C-Scan/G0_S1_XY_Int.tiff', Int)

## to save a B_Scan:
#pytdms.Save_Image('Raw_C-Scan/G0_S1_XY_Int.tiff', Int[50])

# def read_tdms(filename, A_scan_num, B_scan_num):
#     ## Read the TDMS data from the PS-OCT system and write to a C-Scan matrix.

#     ## inputs filename = TDMS file location, A_scan_num is the number of A_Scans in each B_Scan and B_scan_num is the number of B_Scans in the C_Scan.
#     tdms_file = TdmsFile.read(filename) ##import the data as a TDMS
    
#     data = np.squeeze(tdms_file.as_dataframe().to_numpy())
#     #data =  tdms_file.Object('Untitled', tdms_file.group_channels('Untitled')[0].channel).data ## Extract the data
    
#     A_scan_length = int(len(data)/B_scan_num/A_scan_num) # calculate A_scan length
#     data.resize((B_scan_num,A_scan_num,A_scan_length))
#     C_scan = np.array(data)     
#     return(C_scan)

def read_tdms(filename, A_scan_num, B_scan_num):
    ## Read the TDMS data from the PS-OCT system and write to a C-Scan matrix.

    ## inputs filename = TDMS file location, A_scan_num is the number of A_Scans in each B_Scan and B_scan_num is the number of B_Scans in the C_Scan.
    tdms_file = TdmsFile.read(filename) ##import the data as a TDMS
    
    data = np.squeeze(tdms_file.as_dataframe().to_numpy())
    #data =  tdms_file.Object('Untitled', tdms_file.group_channels('Untitled')[0].channel).data ## Extract the data
    
    A_scan_length = int(len(data)/B_scan_num/A_scan_num) # calculate A_scan length
    data.resize((B_scan_num,A_scan_num,A_scan_length))
    C_scan = np.array(data)     
    return(C_scan)


def Scan_processing_3D(ch0,ch1,padSize):
    #### Turn the channel data into Intensity and Birefringence matrices

    ## Inputs 3D numpy matrices for each channel. Outputs are the Intenstiy and Retardation  3D matrices. If save == True, the processed data is saved as a numpy array using the provided name.
    Intensity =[]
    Retardation = []
    #Ch0Complex = []
    #Ch1Complex =[]
    ### for each B_scan
    
    for x in range(0,len(ch0[:,0,0])):

        ### for each channel compute the Intensity (Int) and Retardation (Ret).
        bCh0 = ch0[x,:,:]
        bCh1 = ch1[x,:,:]
        Int, Ret = Scan_processing_2D(bCh0,bCh1,padSize)

        ### append the B_scan to the C_scan
        #Ch0Complex.append(fftCh0)
        #Ch1Complex.append(fftCh1)
        Intensity.append(Int)
        Retardation.append(Ret)
        
    return np.array(Intensity), np.array(Retardation)#, np.array(Ch0Complex), np.array(Ch1Complex)

def Scan_processing_2D(bCh0, bCh1,padSize):
    

    ## Inputs 2D numpy matrices for a B_scan in each channel. Outputs are the Intenstiy and Retardation  2D matrices.
    ch0Padded =  np.pad(bCh0,((0,0),(padSize,padSize)), 'constant')
    ch1Padded =  np.pad(bCh1,((0,0),(padSize,padSize)), 'constant')
    hanning = np.hanning(np.size(bCh0,1))
    hanPad = np.pad(hanning, (padSize,padSize), 'constant')
    
    
    for x in range(len(bCh0)):
        ch0Padded[x] = hanPad*ch0Padded[x]
        ch1Padded[x] = hanPad*ch1Padded[x]
        

    fftCh0raw = np.fft.fft(ch0Padded)
    fftCh1raw = np.fft.fft(ch1Padded)
    start = int(0.00*np.size(ch0Padded,1))
    stop = int(0.5*np.size(ch1Padded,1))
    fftCh0 = np.rot90(fftCh0raw[:,start:stop],3)
    fftCh1 = np.rot90(fftCh1raw[:,start:stop],3)
    

    #Now create the image from the data
    #Int = np.sqrt(np.abs(fftCh0)**2 + np.abs(fftCh1)**2)
    Int = np.abs(fftCh0)**2 + np.abs(fftCh1)**2
    Int = Int[:,0:680]
    Ret = np.arctan(np.abs(fftCh0)/np.abs(fftCh1))
    Ret = Ret[:,0:680]
    return(Int, Ret)#,fftCh0raw,fftCh1raw)


    