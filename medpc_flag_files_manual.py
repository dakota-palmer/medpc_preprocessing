# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:03:16 2022

@author: Dakota
"""

#%% Search for specific errors in raw MED-PC .txt data files

# ~~ this will be highly customized script for a specific dataset !

# TODO: Not actually cleaning raw data file .txts

# TODO: - support independent cleaning of multiple excel files ... currently make single combined output at end but probs can just extend allFiles loop


#%% Import dependencies
import pandas as pd
import glob
import os

import seaborn as sns


#%% Define data paths for input/output

# root directory where this script is
dataPathRoot= os.getcwd()

# your path to folder containing excel files with MedPC data
dataPathInput= dataPathRoot+'/_manual_flag_files/_input/'

# output folder, here new folder to save output plots etc
dataPathOutput= dataPathRoot+'/_manual_flag_files/_output/'

#output folder for log of files with 'cleaned' subjects
dataPathLogs= dataPathRoot+'/_manual_flag_files/_output/_flagged_files/'


#%%----- VP-OPTO dataset-------


#%% ID and import raw data .xlsx

# set all .xls files in your folder to list
allfiles = glob.glob(dataPathInput + "*.xls*")

#initialize list to store data from each file
dfRaw = pd.DataFrame()

#define columns in your .xlsx for specific variables you want (e.g. A:Z for all, but may be double letters if many variables)
colToImport= 'A:N' #assume first few columns have metadata desired

#for loop to aquire all excel files in folder
for excelfiles in allfiles:
    #read all sheets by specifying sheet_name = None
    #Remove any variables you don't want now before appending!
    raw_excel = pd.read_excel(excelfiles, sheet_name= None, usecols=colToImport)
    
    #append all sheets into single df
    for sheet in raw_excel:
        dfRaw= dfRaw.append(raw_excel[sheet], ignore_index=True)
    
#%% Fix dtypes


# convert StartDate column to datetime for better readability in plots (and mathematical date comparisons)
# dfRaw.StartDate= pd.to_datetime(dfRaw['StartDate'], format='%y%m%d')

#convert StartDate column to int for mathematical date comparisons
dfRaw.StartDate= dfRaw.StartDate.astype(int)

#convert medpc_preprocessing_note to str if not already
dfRaw.medpc_preprocessing_note= dfRaw.medpc_preprocessing_note.astype(str)
# replace nan from excel with None (so can add to existing strings)
ind=[]
ind= dfRaw.medpc_preprocessing_note=='nan'
dfRaw.loc[ind, 'medpc_preprocessing_note']= ''
    
#%% Make a column to flag files
 # for "Notes" of files where subject is changed
#TODO: consider changing raw data file too
    
#assume this column exists already
# dfRaw['medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note
dfRaw['flagged']=None



#%% - Correct mislabeled OM20 files

#%% if labelled OM2 and beyond ~May 2019, flag and correct to OM20 
 
ind= []

# ind= (dfRaw.Subject=='OM2') & (dfRaw.StartDate > '2019-05-01')
ind= (dfRaw.Subject=='OM2') & (dfRaw.StartDate > 190501)

## viz
# test= dfRaw.loc[ind,:]

flagStr= '_manually_corrected_subject_typo'

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.loc[ind,'medpc_preprocessing_note']+flagStr
dfRaw.loc[ind,'flagged']=1

#manually correct Subject
dfRaw.loc[ind,'Subject']= 'OM20'

#%% if labelled OM10 and beyond ~November 2019, flag and correct to OM20
 
ind= []

# ind= (dfRaw.Subject=='OM10') & (dfRaw.StartDate > '2019-11-01')
ind= (dfRaw.Subject=='OM10') & (dfRaw.StartDate > 191101)


## viz
test= dfRaw.loc[ind,:]

flagStr= '_manually_corrected_subject_typo'

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note+flagStr
dfRaw.loc[ind,'flagged']=1

#manually correct Subject
dfRaw.loc[ind,'Subject']= 'OM20'

 
 #%% - Correct O27 file

ind= []

ind= (dfRaw.Subject=='O27')


## viz
test= dfRaw.loc[ind,:]

# flagStr= '_manually_corrected_subject_typo'

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note+flagStr

dfRaw.loc[ind,'flagged']=1

#manually correct Subject
dfRaw.loc[ind,'Subject']= 'OV27'


 #%% - Correct OV37 file

ind= []

ind= (dfRaw.Subject=='OV37')


## viz
test= dfRaw.loc[ind,:]

# flagStr= '_manually_corrected_subject_typo'

dfRaw.loc[ind,'medpc_preprocessing_note']= dfRaw.medpc_preprocessing_note+flagStr

dfRaw.loc[ind,'flagged']=1

#manually correct Subject
dfRaw.loc[ind,'Subject']= 'OV27'

#%% - Make table to save flagged/corrected files
flagged= pd.DataFrame

ind= []

ind= dfRaw.flagged==1

flagged= dfRaw.loc[ind,'flagged']


#%% save flagged files as csv

flagged= dfRaw.loc[ind,:]

import datetime
fileName= '_LOG_Files_flagged_manual_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) 

os.chdir(dataPathLogs)

# flagged.to_csv(strLog)

#save as excel sheet 
fileName= fileName+'.xlsx'

flagged.to_excel(fileName, index=False)


os.chdir(dataPathRoot)


#%% Save new .xlsx with corrections


#drop flagged column
dfRaw= dfRaw.drop('flagged', axis=1)
 
#keep original excel sheet name, add '_cleaned'
# TODO: this just grabs first excel file name in allFiles
fileName= os.path.basename(allfiles[0])

#remove prior .xslx from filename (TODO: assumes exactly .xlsx)
fileName=fileName[0:-5]

# thisFileName= os.path.basename(fileName)


fileName= fileName+'_manual_corrections'

os.chdir(dataPathOutput)


#save as excel sheet 
fileName= fileName+'.xlsx'

dfRaw.to_excel(fileName)

os.chdir(dataPathRoot)

