import sys 
import os 
import numpy as np
import matplotlib.pyplot as plt      
import TdmsCodeGallery as pytdms


def loadData(dataLocation,npy,output,variableName,A_scan_num,B_scan_num,padSize):
    Int = []
    Ret = []
    Ch0Complex=[]
    Ch1Complex=[]
    check = checkDirectory(dataLocation, npy,output, variableName,autoProcess=True)
    if check==0:
        print('We are good to go. Loading in channel spectra now!')
        Int = np.load(dataLocation + npy + '\\' + variableName + '\Int' +  '.npy')
        print('Loaded in Int')
        Ret = np.load(dataLocation + npy + '\\' + variableName + '\Ret' +  '.npy')
        print('Loaded in Ret')
        #Ch0Complex = np.load(dataLocation + npy + '\\' + variableName + '\Ch0Complex.npy')
        print('Loaded in Ch0')
        #Ch1Complex = np.load(dataLocation + npy + '\\' + variableName + '\Ch1Complex.npy')
        print('Loaded in Ch1')
    elif check==1:
        print('We are reading the TDMS files and making numpy files for future')
        ch0  =  pytdms.read_tdms(dataLocation + '\Ch0_' + variableName + '.tdms',  A_scan_num, B_scan_num)
        ch1  =  pytdms.read_tdms(dataLocation + '\Ch1_' + variableName + '.tdms',  A_scan_num, B_scan_num)            
        Int, Ret = pytdms.Scan_processing_3D(ch0,ch1,padSize)
        np.save(dataLocation + npy + '\\' + variableName + '\Int' +   '.npy', np.array(Int))
        np.save(dataLocation + npy + '\\' + variableName + '\Ret' +   '.npy', np.array(Ret))
        # np.save(dataLocation + npy + '\\' + variableName + '\Ch0Complex' +   '.npy', np.array(Ch0Complex))
        # np.save(dataLocation + npy + '\\' + variableName + '\Ch1Complex' +   '.npy', np.array(Ch1Complex))
    elif check==2:
        print('Check Directory Function Did Not Work')
    return(Int,Ret)#,Ch0Complex,Ch1Complex)    



def checkDirectory(dataLocation,npy,output,variableName,autoProcess=True):
    if os.path.isdir(dataLocation + npy + '\\' + variableName):
        if os.path.isfile(dataLocation + npy + '\\' + variableName + '\Int' +   '.npy') and os.path.isfile(dataLocation + npy + '\\' + variableName + '\Ret' +   '.npy'):
            print('All npy files are present')
            check=0
            if os.path.isdir(dataLocation + output + '\\' + variableName): # So we have the numpy files, but do we have an output folder to put our results eventually?
                print('Your output data will be saved in: ' + output + '\\' + variableName)     
            else:
                if os.path.isdir(dataLocation + output): #Check if there is a output files directory in the sample folder
                    makeDir(dataLocation, output, '\\' + variableName) #make the directory if we don't have one for the specific trial output folder
                else: #If there is no output folder what so ever then we  have to make both.
                    makeDir(dataLocation, '', output)
                makeDir(dataLocation, output, '\\' + variableName)
    
        elif os.path.isfile(dataLocation + '\Ch0_' + variableName + '.tdms') and os.path.isfile(dataLocation + '\Ch1_' + variableName + '.tdms')  :
            if not os.path.isdir(dataLocation + npy ):
                makeDir(dataLocation, '\\',npy)
            if not os.path.isdir(dataLocation + npy  + '\\' + variableName):
                makeDir(dataLocation, npy, '\\' + variableName)
            if not os.path.isdir(dataLocation + output ):
                makeDir(dataLocation, '\\',output)
            if not os.path.isdir(dataLocation + output  + '\\' + variableName):
                makeDir(dataLocation, output, '\\' + variableName)        
            check = 1
            
    else:
            if not os.path.isdir(dataLocation + npy ):
                makeDir(dataLocation, '\\',npy)
            if not os.path.isdir(dataLocation + npy  + '\\' + variableName):
                makeDir(dataLocation, npy, '\\' + variableName)
            if not os.path.isdir(dataLocation + output ):
                makeDir(dataLocation, '\\',output)
            if not os.path.isdir(dataLocation + output  + '\\' + variableName):
                makeDir(dataLocation, output, '\\' + variableName)        
            check = 1
    return(check)

def makeDir(dataLocation, name, folderName): #make the folder
    os.makedirs(dataLocation + name + folderName)
    print('A folder was made and called: '+ name + folderName)



