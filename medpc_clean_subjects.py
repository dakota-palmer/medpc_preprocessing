# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:05:33 2022

@author: Dakota
"""

#%% Make all variations of Subject strings consistent 
#% Correct variations in subject names (case, punctuation, spaces)

# input = excel sheet, output= 'cleaned' excel sheet

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
dataPathOutput= dataPathRoot+'/_medpc_excel_file_overview/_output/'

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


test= dfRaw.loc[ind,:]

# test= subjectsOG.unique()
# test2= dfRaw.SubjectCleaned.unique()


