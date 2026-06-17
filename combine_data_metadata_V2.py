#Elen Golightly 4/3/26
#script to combine metadata variable labels with data as 2nd row
#this is so the PII checker can scan the labels for concerns
#and to inform the human reviewer with the outputs

import pandas as pd
import numpy as np

def userinput(input_file, metadata_file):

    dat_df = pd.read_csv(input_file, encoding = "utf-8-sig", low_memory = False)
    met_df = pd.read_excel(metadata_file)

#convert blanks to NULL
#    print("converting blank cells to NULL...")
    dat_df = dat_df.replace(r'^\s*$', np.nan, regex=True).fillna("NULL")
    met_df = met_df.replace(r'^\s*$', np.nan, regex=True).fillna("NULL")

#get metadata variable names and labels
    meta_varnames = met_df['var_name']
    meta_varlabels = met_df['var_label']

#create series with varnames as index and labels
    series2 = pd.Series(data=meta_varlabels.values, index=meta_varnames.values)
    series2_aligned = series2.reindex(dat_df.columns)
    #deal with additional metadata variables that may not be present for specific data table
    series2_aligned = series2_aligned.fillna('')
#get new row with labels
    labrow = pd.DataFrame([series2_aligned])

#get 1st row of data file (for variable names) and the rest of the data
    dat_header = dat_df.iloc[:0,:]
    dat_content = dat_df.iloc[0:,:]
    

#combined data file:
    dat_comb = pd.concat([dat_header, labrow, dat_content], ignore_index=True)
    print("Data has been combined with labels ready for PII search...")
    return(dat_comb)





