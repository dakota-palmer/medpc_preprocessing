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

    
#%%TODO:  Move files into sub-folders based on manual MSN grouping
# make custom groups that should be grouped together using your MSNs
# want to group for common row profile / data extraction methods

# groups=['_MSNs_MagTrain','MSNs_DSTask','MSNs_DSTaskOpto','MSNs_ChoiceTaskOpto','MSNs_ICSS','MSNs_Other']

MSNs_MagTrain= [' JMRmagtraining_30ITI30_licks_Input6', ' JMRmagtraining_30ITI30_licks_ver2']

MSNs_DSTask= [' DS NS Training Stage 1', ' DS NS Training Stage 2', ' DS NS Training Stage 3', 
              ' DS NS Training Stage 4', ' DS NS Devaluation Training', ' PortEventDSFinalStageCC',
              ' Opto STAGE 1 DS Task 11_3_2020',
              ' Opto Stage 2 DS Task 11_3_2020',
              ' Opto Stage 3 DS Task 11_3_2020',
              ' Opto STAGE 2 DS Task 11_18_2020',
              ' Opto Stage 4 DS Task 11_3_2020',
              ' Opto Final Stage DS Task 11_3_2020',]

MSNs_DSTaskOpto= [' PulsePal Opto Laser DS Code', ' PulsePal Gated Stimulation']

MSNs_ChoiceTaskOpto= [' Dani Lever Press', ' Box1LeverPress', ' Box1LeverPressSWITCHED',
                      ' DaniLeverPressSWITCHED', ' BOX1ChristelleForcedLeverOpto', ' ChristelleForcedLeverOpto']

MSNs_ICSS= [' Christelle Opto ICSS']

MSNs_Other= [' Opto Stimulation Protocol (cFos)']


# Make a dataframe of files and corresponding MSNs, make new column for group
df= pd.DataFrame()

df['file']= allFiles
df['fileMSN']= allFilesMSN

df['fileMSNgroup']= None

# go through and assign group if this MSN is in list
ind= []
ind= df.fileMSN.isin(MSNs_MagTrain)
df.loc[ind, 'fileMSNgroup']= 'MSNs_MagTrain'

ind= []
ind= df.fileMSN.isin(MSNs_DSTask)
df.loc[ind, 'fileMSNgroup']= 'MSNs_DSTask'

ind= []
ind= df.fileMSN.isin(MSNs_DSTaskOpto)
df.loc[ind, 'fileMSNgroup']= 'MSNs_DSTaskOpto'

ind= []
ind= df.fileMSN.isin(MSNs_ChoiceTaskOpto)
df.loc[ind, 'fileMSNgroup']= 'MSNs_ChoiceTaskOpto'

ind= []
ind= df.fileMSN.isin(MSNs_ICSS)
df.loc[ind, 'fileMSNgroup']= 'MSNs_ICSS'

ind= []
ind= df.fileMSN.isin(MSNs_Other)
df.loc[ind, 'fileMSNgroup']= 'MSNs_Other'


groupsUnique= df.fileMSNgroup.unique()
for thisMSNgroup in groupsUnique:
    
    #make a new folder for this MSN in output directory   
    # nest within a new _Manual_Groups folder
    pathThisMSN= os.path.join(dataPathOutput+'_Manual_Groups/', thisMSNgroup)
    
    os.mkdir(pathThisMSN)
        
    # #change to pandas series for convenience
    # allFiles= pd.Series(allFiles)
    # allFilesMSN= pd.Series(allFilesMSN)

    # #get data files with this MSN and copy them into folder
    # ind= []
    # ind= allFilesMSN==thisMSN    
    
    ind= df.fileMSNgroup==thisMSNgroup
    
    for thisFile in df.loc[ind,'file']:
        fileNameOG= os.path.basename(thisFile)
        
        #copy files into new folder
        path=[]
        path= os.path.join(pathThisMSN, fileNameOG)
                
        shutil.copy(os.path.abspath(thisFile), path)
