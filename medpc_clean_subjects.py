# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:05:33 2022

@author: Dakota
"""

#%% Make all variations of Subject strings consistent 
#% Correct variations in subject names (case, punctuation, spaces)

# input = excel sheet, output= 'cleaned' excel sheet
#TODO: ( not actually cleaning raw data file .txts)

#%% Import dependencies
import pandas as pd
import glob
import os

import seaborn as sns

#%% Define data paths for input/output

# root directory where this script is
dataPathRoot= os.getcwd()

# your path to folder containing excel files with MedPC data
dataPathInput= dataPathRoot+'/_medpc_excel_file_overview/_input/'

# output folder, here new folder to save output plots etc
dataPathOutput= dataPathRoot+'/_clean_subjects/_output/'

#output folder for log of files with 'cleaned' subjects
dataPathLogs= dataPathRoot+'/_clean_subjects/_output/_flagged_files/'

#%% TODO:
    #- support independent cleaning of multiple excel files ... currently make single combined output at end but probs can just extend allFiles loop

#%% ID and import raw data .xlsx

# set all .xls files in your folder to list
allfiles = glob.glob(dataPathInput + "*.xls*")

#initialize list to store data from each file
dfRaw = pd.DataFrame()

#define columns in your .xlsx for specific variables you want (e.g. A:Z for all, but may be double letters if many variables)
colToImport= 'A:J' #assume first few columns have metadata desired

#for loop to aquire all excel files in folder
for excelfiles in allfiles:
    #read all sheets by specifying sheet_name = None
    #Remove any variables you don't want now before appending!
    raw_excel = pd.read_excel(excelfiles, sheet_name= None, usecols=colToImport)
    
    #append all sheets into single df
    for sheet in raw_excel:
        dfRaw= dfRaw.append(raw_excel[sheet], ignore_index=True)
    
#%% Make a column for "Notes" of files where subject is changed
#TODO: consider changing raw data file too
    
dfRaw['medpc_preprocessing_note']= ''

#%% Clean subject names

subjectsOG= dfRaw.Subject

#make new column for 'cleaned' subjects
dfRaw.SubjectCleaned= dfRaw.Subject

#-- strip() to remove any extra spaces
subjectStripped= dfRaw.Subject.str.strip()

# make note of files where subjects were changed as result of strip()
ind=[]
ind= dfRaw.Subject!=subjectStripped

# test= dfRaw[ind] #viz

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note + '_subjectStripped'

# save new subject to column
dfRaw.loc[ind,'SubjectCleaned']= subjectStripped

#-- correct variations in Case
# simply make all uppercase

subjectsUpper= subjectsOG.str.upper()

# make note of files where subjects changed as result of upper()
ind=[]
ind= dfRaw.Subject!=subjectsUpper

# test= dfRaw[ind] #viz

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note + '_subjectUpperCased'

# save new subject to column
dfRaw.loc[ind,'SubjectCleaned']= subjectsUpper


#-- get report of files with cleaned subject
ind= []
# ind= ~dfRaw.medpc_preprocessing_note.isnull()
ind= ~(dfRaw.medpc_preprocessing_note == '')



#%% save flagged files as csv

flagged= dfRaw.loc[ind,:]

import datetime
fileName= '_LOG_Files_subjectsCleaned_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) 

os.chdir(dataPathLogs)

# flagged.to_csv(strLog)

#save as excel sheet 
fileName= fileName+'.xlsx'

flagged.to_excel(fileName)


os.chdir(dataPathRoot)


#%% Overwrite original subjects with 'cleaned' and save new .xlsx

# overwrite OG column and drop new column
dfRaw.Subject= dfRaw.SubjectCleaned

dfRaw= dfRaw.drop('SubjectCleaned', axis=1)
 
#keep original excel sheet name, add '_cleaned'
# TODO: this just grabs first excel file name in allFiles
fileName= os.path.basename(allfiles[0])

#remove prior .xslx from filename (TODO: assumes exactly .xlsx)
fileName=fileName[0:-5]

# thisFileName= os.path.basename(fileName)


fileName= fileName+'_cleanedSubjects'

os.chdir(dataPathOutput)


#save as excel sheet 
fileName= fileName+'.xlsx'

dfRaw.to_excel(fileName, index=False)

os.chdir(dataPathRoot)


# import datetime
# strLog= '_LOG_Files_subjectsCleaned'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) +'.txt'

# with open(strLog, 'w') as f: 
#      for line in test:
#             f.write(f"{line}\n")          



# test= subjectsOG.unique()
# test2= dfRaw.SubjectCleaned.unique()


