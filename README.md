# medpc_preprocessing
A collection of python scripts for vizualizing, cleaning, and organizing raw data files from Med Associates (MED-PC)


#------Suggested workflow ---- #
Always back OG raw data up and work only on copies.
2022-01-19, Haven't integrated these fully but some ideas:

-Raw .TXT file data tools

1) _find_and_split_duplicates.py - To automatically ID and split combined files with multiple subjects into separate files. Also automatically IDs and quarantines files with missing/blank subjects
2) _medpc_flag_files_manual.py - If you're aware of specific conditions of files you want to flag and quarantine for manual review (e.g. specific box/subject/MSN) 
3) medpc_sort_by_MSN.py - Sort raw data files into subfolders based on MSN. Useful for grouping files with similar data organization prior to extraction into excel 

-Extracted excel sheet data tools

1) _medpc_clean_subjects.py- To standardize subject IDs, removes variation in capitalization/spaces 
2) _excel_file_overview.py- To vizualize, gives broad overview of your data's timeline

#------ Folder setup / pathing ----- #
As of 2022-12-9, pathing for _find_and_split_duplicates.py is relative so want to download this repository and within add subfolders to ultimately look like:

- medpc_preprocessing-main

  --- _find_and_split_duplicates
  
      --- _input
      
      --- _output
      
            --- _split_files
            
            --- _flagged_file_quarantine
