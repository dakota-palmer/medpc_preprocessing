# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:07:48 2022

@author: Dakota
"""

#% This Script will plot training history for each subject from excel sheet
#% ~~~  Assumes you have Subject, StartDate, Box, and MSN columns in your spreadsheet ~~~~
# ~~~ should pull all sheets from all .xslx in the dataPathInput folder ~~~

#% After running medpc2excel, let's vizualize the output to screen for errors
#e.g. duplicate sessions, incorrect dates, subject name variations, MSN name variations, box/equipment variations


#%% TODO

# -- pandas profiling ? easy automated report of behavioral variables to find/flag outlier sessions (e.g. lickometer/PE detector malfunctions)
# -- make simpler training phases based on MSN dictionary (should make outliers/overall patterns more clear)

if __name__ == '__main__':
    #this is added for pandas-profiling
    
    #%% Import dependencies
    import pandas as pd
    import glob
    import os
    
    import seaborn as sns
    
    #%% Vizualize session history for each subject
    #- plot start date and MSN by subject
    
    
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
        
    
    #%% ~~~ PANDAS PROFILING ~~~~~~~
    
    
    
    #%% Use pandas profiling
    # This might be a decent way to quickly view behavior session results/outliers if automated
    # note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install
    
    # from pandas_profiling import ProfileReport
    
    # import matplotlib.pyplot as plt
    
    
    # # profile = ProfileReport(dfRaw, title='MEDPC_excel_file_overview', explorative = False)
    # # profile = ProfileReport(dfRaw, explorative = False)
    # profile = ProfileReport(dfRaw, explorative=True, n_freq_table_max=250)

    
    # os.chdir(dataPathOutput)
    
    
    # # save profile report as html
    # profile.to_file('pandasProfile-MEDPC_excel_file_overview.html')
    
    
    # os.chdir(dataPathRoot)
    
    
    #%% Convert datetime variables 

    #make new column with StartDate and StartTime combined prior to conversion
    #convert to string prior to combining
    dfRaw.StartDate= dfRaw.StartDate.astype('string')
    dfRaw.StartTime= dfRaw.StartTime.astype('string')

    dfRaw['StartDateTime']= dfRaw.StartDate+dfRaw.StartTime

    dfRaw.StartDateTime= dfRaw.StartDate+dfRaw.StartTime
    
        
    dfRaw.StartDateTime= pd.to_datetime(dfRaw['StartDateTime'], format='%y%m%d%H%M%S')

    # convert StartDate column to datetime for better readability in plots
    dfRaw.StartDate= pd.to_datetime(dfRaw['StartDate'], format='%y%m%d')
    
    # simply keep StartTime as int (because for some reason was inserting default year/month as 1900)
    dfRaw.StartTime= dfRaw.StartTime.astype('int')

        
    #%% ~~~ PLOTS ~~~~~~~
    
    #%% Plot of all files by subject
        
    g= sns.relplot(data= dfRaw, x='StartDate', y='Subject', hue='MSN', kind='scatter')
    
    g.map_dataframe(sns.lineplot,data= dfRaw, units='Subject', estimator=None, x='StartDate', y='Subject', hue='MSN', alpha=0.5)



    #%% filter out nans (plotly doesn't like nans)?
    ind= dfRaw.Subject.isnull()
    
    test= dfRaw.loc[~ind,:]
    
    dfRaw= test
    
    ind= dfRaw.MSN.isnull()
    
    test2= dfRaw.loc[~ind,:]
    
    ind= dfRaw.isnull()
    test3= dfRaw[ind]

    #%% Sort data by StartDateTime
    # dfRaw= dfRaw.sort_values('StartDateTime')


    #%% Use Plotly to save interactive html
     
    # dfRaw.columns= dfRaw.columns.str.strip()
    
 
    
    import plotly.express as px #plotly is good for interactive plots (& can export as nice interactive html)
    import plotly.io as pio

    
    
    # fig= px.line(dfRaw, x= 'StartDate', line_group='Subject', y='Subject', color='MSN', markers=True)

    # fig.show() 
    # #plotly export as interactive html
    # figName= 'train history by subject with MSN'
    # fig.write_html(dataPathOutput+figName+'.html')
            
      
    fig= px.line(dfRaw, x= 'StartDateTime', line_group='Subject', y='Subject', color='MSN', markers=True)

    fig.show() 
    #plotly export as interactive html
    figName= 'train history by subject with MSN_dateTime'
    fig.write_html(dataPathOutput+figName+'.html')
    
    
    # fig= px.line(dfRaw, x= 'StartDate', line_group='Subject', y='Subject', color='Box', markers=True)

    # fig.show() 
    # #plotly export as interactive html
    # figName= 'train history by subject with Box'
    # fig.write_html(dataPathOutput+figName+'.html')
    
    
    fig= px.line(dfRaw, x= 'StartDateTime', line_group='Subject', y='Subject', color='Box', markers=True)

    fig.show() 
    #plotly export as interactive html
    figName= 'train history by subject with Box_dateTime'
    fig.write_html(dataPathOutput+figName+'.html')
    
    
    
    # fig= px.line(dfRaw, x= 'StartDate', line_group='Subject', y='Subject', color='Subject', markers=True)

    # fig.show() 
    # #plotly export as interactive html
    # figName= 'train history by Subject'
    # fig.write_html(dataPathOutput+figName+'.html')
    
    fig= px.line(dfRaw, x= 'StartDateTime', line_group='Subject', y='Subject', color='Subject', markers=True)

    fig.show() 
    #plotly export as interactive html
    figName= 'train history by Subject_dateTime'
    fig.write_html(dataPathOutput+figName+'.html')
    

    
    # fig= px.line(dfRaw, x= 'StartDate', line_group='Subject', y='Box', color='Subject', markers=True)

    # fig.show() 
    # #plotly export as interactive html
    # figName= 'train history by Box with Subject Lines'
    # fig.write_html(dataPathOutput+figName+'.html')
    
    

    # fig= px.line(dfRaw, x= 'StartDate', line_group='Box', y='Box', color='Subject', markers=True)

    # fig.show() 
    # #plotly export as interactive html
    # figName= 'train history by Box'
    # fig.write_html(dataPathOutput+figName+'.html')
    
    
    
    #%% Add unique fileID for each session (subject & date)
    #should be unecessary, each row here should be unique file
    
    # #sort by date and subject
    # # test= df.sort_values(['date','subject'])
    # dfRaw= dfRaw.sort_values(['date','subject'])
    
    
    # dfRaw.loc[:,'fileID'] = dfRaw.groupby(['date', 'subject']).ngroup()
    
        
    
    #%% Plot 
