# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:05:33 2022

@author: Dakota
"""

#%% Sort all raw data files based on MSN.
# MPC data extraction using row profiles should operate based on MSN. 
# For easy batch processing, sort raw data files into subfolders based on MSN.

# Read all raw MPC data files, get the MSN, and move into new subfolder

# Assumes this is done after splitting combined data files (only searching for 1 "MSN:" per file)

#%% TODO

#- integrate into a workflow
#- can change to more dynamic sub-folder assignment across MSNs at end


#%% Import dependencies
import glob

# from datetime import date
import datetime

import os

import shutil

import pandas as pd
      
#%% Define paths and string to use for splitting
#path to the .txt datafiles saved by MedPC
# dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/'

# dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/_test/'

# root directory where this script is
dataPathRoot= os.getcwd()

# folder containing input .txt files
# dataPathInput= dataPathRoot+'/_find_and_split_duplicates/_input/'
dataPathInput= r'F:\_Github\Richard Lab\data-vp-opto\_MPC_data\_MPC_data_Corrected/'

# output folder, here new folder to save sort output files
# dataPathOutput= dataPathRoot+'/_find_and_split_duplicates/_output/_split_files'
dataPathOutput= dataPathInput+'/_sorted_by_MSN/'

#% Define string to search/split
splitStr= 'MSN:'

#%% Get list of all .txt files in dataPathInput

# os.chdir(dataPathInput)

allFiles= glob.glob(dataPathInput+"*.txt")

#%% Read data file as string, find splitStr and save 
#read the MSN from this file, save into list
allFilesMSN= []

#keep a list of files which are flagged and split
# filesFlagged= []

for thisFile in allFiles:
    
    content= open(thisFile).read()
    
    # if splitStr in content:
    #     print('str exists')
    
    
    
    #count # of string occurrences in file
    n= content.count(splitStr)

    #normally a file should have 1 splitStr, if >0 (python counts starting with 0) warn user
    if n>1:
        print('!~~~~~~ duplicate MSN found--'+ thisFile+ '~~~~~~~~!')


    #split the raw data file into lines and get the line where "MSN:" is present
    content= content.splitlines()
    
    for line in content:
        if splitStr in line:
            thisMSN= line.split(splitStr)[1]
            break #stop reading once MSN is found
    
    #append thisMSN to list 
    allFilesMSN.append(thisMSN)    
    

#%% Move files into sub-folders based on their unique MSN
# do this after loop so can support more dynamic assignment based on MSN 
# (e.g. could do something like if MSN contains 'Mag Training' move all together into single folder) 
uniqueMSN= pd.unique(allFilesMSN)      

for thisMSN in uniqueMSN:
    
    #make a new folder for this MSN in output directory   
    pathThisMSN= os.path.join(dataPathOutput, thisMSN)
    
    os.mkdir(pathThisMSN)
        
    #change to pandas series for convenience
    allFiles= pd.Series(allFiles)
    allFilesMSN= pd.Series(allFilesMSN)

    #get data files with this MSN and copy them into folder
    ind= []
    ind= allFilesMSN==thisMSN    
    
    for thisFile in allFiles[ind]:
        fileNameOG= os.path.basename(thisFile)
        
        #copy files into new folder
        path=[]
        path= os.path.join(pathThisMSN, fileNameOG)
                
        shutil.copy(os.path.abspath(thisFile), path)

    


