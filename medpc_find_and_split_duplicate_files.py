# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:14:38 2022

@author: Dakota
"""

#%% dependencies
import glob

from datetime import date

#%% 
# in MedPC, sometimes data files are auto-appended into single .txt due to user error (e.g. user forgets to save "subject" field)
# find these files and split them into individual files


#%% Define paths and string to use for splitting
#path to the .txt datafiles saved by MedPC
# dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/'

dataPathInput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/_test/'


# output folder, here new folder to save split output files
# NOTE: for now this is just saving alongside the original data files
# dataPathOutput= r'./_output/split_files/'
dataPathOutput= r'C:/Users/Dakota/Desktop/_christelle_opto_mpc-data/_output/split_files/'

#% Define string to search/split

splitStr= 'Start Date:'

#%% Get list of all .txt files in dataPathInput

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
    
    #normally a file should have 1 splitStr, if >0 (python counts starting with 0) split the file at each occurrence
    if n>1:
        print('!~~~~~~ duplicate data found--'+ thisFile+ '~~~~~~~~!')
        
        #flag this file, add to list
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
            ind= thisFile.index('.txt')        
            thisSplitName= thisFile[:ind]+ strFlagFilename + thisFile[ind:]

            # thisSplitName= dataPathOutput+thisSplitName
            

            # contentSplit[thisSplit]= strFlagFilename+contentSplit[0]+contentSplit[thisSplit]

            #save into separate files
            # NOTE: for now this will save alongside the original file
            #TODO: control specific output folder, having issues with strings e.g. need raw string to convert \ to /
                        
            with open(thisSplitName, 'w') as f:
                
                f.write(contentSplit[thisSplit])
                                
                
      
 #%% Save a log of all the files flagged

strLog= str(date.today()) + '_Files_flagged_duplicates'

with open(strLog, 'w') as f: 
     for line in filesFlagged:
            f.write(f"{line}\n")          


