# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:14:38 2022

@author: Dakota
"""

#%% dependencies
import glob

# from datetime import date
import datetime

import os

import shutil

#%% 
# in MedPC, sometimes data files are auto-appended into single .txt due to user error (e.g. user forgets to save "subject" field)
# find these files and split them into individual files

#%% TODOs:
    
    #-- Deal with duplicate dates / date correction
        #for some reason some files have appended data from different Start Dates... the new Split file names should reflect the correct start time 
        
#%% Define paths and string to use for splitting
#path to the .txt datafiles saved by MedPC
# dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/'

# dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/_test/'

# root directory where this script is
dataPathRoot= os.getcwd()

# folder containing input .txt files
dataPathInput= dataPathRoot+'/_find_and_split_duplicates/_input/'

# output folder, here new folder to save split output files
dataPathOutput= dataPathRoot+'/_find_and_split_duplicates/_output/_split_files'

# separate folder to move flagged OG files 
dataPathQuarantine= dataPathRoot+'/_find_and_split_duplicates/_output/_flagged_file_quarantine/'

# dataPathQuarantine= os.path.abspath(dataPathQuarantine)


# dataPathQuarantine= os.path.abspath(os.path.dirname(dataPathQuarantine))

#% Define string to search/split

splitStr= 'Start Date:'

#%% Get list of all .txt files in dataPathInput

# os.chdir(dataPathInput)

allFiles= glob.glob(dataPathInput+"*.txt")

#%% Read data file as string, find splitStr and split 

#keep a list of files which are flagged and split
filesFlagged= []

for thisFile in allFiles:
    
    content= open(thisFile).read()
    
    # if splitStr in content:
    #     print('str exists')
    
    
    #count # of string occurrences in file
    n= content.count(splitStr)
    
    
    # TODO--
    # Check if there is a valid subject - if left empty will read 'Subject .txt'
    strSubjCheck= 'Subject .txt'
    subjPresent= content.count(strSubjCheck)
    
    if subjPresent >=1:
        print('!~~~~~~ blank subject data found--'+ thisFile+ '~~~~~~~~!')
        #flag this file, add to list
        filesFlagged.append(thisFile)
    
    #normally a file should have 1 splitStr, if >0 (python counts starting with 0) split the file at each occurrence
    if n>1:
        print('!~~~~~~ duplicate data found--'+ thisFile+ '~~~~~~~~!')
        
        #flag this file, add to list
        if thisFile not in filesFlagged: #if not already in flagged list due to blank subject
            filesFlagged.append(thisFile)
    
        #split the file at splitStr occurrences.      
        contentSplit= content.split(splitStr)
        
        # Include the splitStr TODO: being cut out 
        #simply add the splitStr to the beginning of each split (was removed initially)
        
        #First split will be the original file name, so only add splitStr to subsequent splits (>=1)
        
        for thisSplit in range(1,len(contentSplit)):
            
            #add splitStr to this new split file
            contentSplit[thisSplit]= splitStr+contentSplit[thisSplit]

            #flag this filename and add to content
            strFlagFilename= '_SplitFile_'+str(thisSplit)+'_'

            #add modified filename to this new split file, flagging for review            
            #find .txt extension and add strFlagFilename before to flag for review
            #overwrite fileName content with flagged filename (do this separately since has newlines etc)
            ind= contentSplit[0].index('.txt')
            contentSplit[0]= contentSplit[0][:ind] + strFlagFilename + contentSplit[0][ind:]

            #also save string filename for saving into new file
            # ind= thisFile.index('.txt')        
            # thisSplitName= thisFile[:ind]+ strFlagFilename + thisFile[ind:]

            # use os.path.basename to isolate file name from rest of path
            thisSplitName= os.path.basename(thisFile) + strFlagFilename + '.txt'
             
            # thisSplitName= dataPathOutput+thisSplitName
            

            # contentSplit[thisSplit]= strFlagFilename+contentSplit[0]+contentSplit[thisSplit]

            #save new split files into separate files 
            os.chdir(dataPathOutput)
            
            with open(thisSplitName, 'w') as f:
                
                f.write(contentSplit[thisSplit])
                       
         
#after splitting,
#move the flagged original files into a quarantine folder

for thisFile in filesFlagged:
# os.chdir(dataPathRoot)

    fileNameOG= os.path.basename(thisFile)
    
    shutil.move(os.path.abspath(thisFile), dataPathQuarantine + fileNameOG)


#back to root directory            
os.chdir(dataPathRoot)
                
      
 #%% Save a log of all the files flagged

strLog= '_LOG_Files_flagged_duplicates_and_blankSubjects_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) +'.txt'

os.chdir(dataPathQuarantine)

with open(strLog, 'w') as f: 
     for line in filesFlagged:
            f.write(f"{line}\n")          


os.chdir(dataPathRoot)
