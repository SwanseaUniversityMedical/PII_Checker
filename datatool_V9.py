# Elen Golightly original 27.1.25
# development 6.1.25
# changes:  1) separating it out to numerical only and mixed (strings or columns with strings and numerical) datasets
#           2) choose input file instead of using path
#           3) separate out flag type and flag reason
#           4) ignore certain flags e.g. drivers liscence
#           5) choose only cells that are <5 counts to run check on.
# development 10.11.25
# changes: 1) introducing streamlit with user input variables - use app_V1.py
# development 19.12.25
# changes: 1) adding scores to output file - removed bc not score in a helpful sense (see notes)
#          2) add custom recognisers
#          3) reduce false positives for numbers = PERSON
# development 26.1.26
# changes: 1) including variable label to help inform human review - DONE
#          2) including search of variable label to help flags e.g. look for >1dec place for label containing "age" - DONE

from typing import List, Optional, Dict, Union, Iterator, Iterable
import collections
from dataclasses import dataclass
import pprint
from collections import defaultdict
from datetime import datetime
import time
import sys
import pandas as pd


from presidio_analyzer import AnalyzerEngine, BatchAnalyzerEngine, RecognizerResult, DictAnalyzerResult
from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine
from presidio_anonymizer.entities import EngineResult
from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    EntityRecognizer,
    Pattern,
    RecognizerResult,
)
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine, SpacyNlpEngine, NlpArtifacts
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
import re

#add custom recognisers 
from custom_date_recogniser import get_date_recogniser 
from custom_varlabel_recogniser import keyword_recogniser 


#track time taken for tool to run
start = time.time()

def userinput(combined_data, threshold, restrictions):
    # get data
    orig_data = combined_data #getting this from combine_data_metadata.py so data has var labels in 2nd row
    print("Data loaded.")
 
    data_only = orig_data.iloc[1:].reset_index(drop=True) #varnames and data only, ignore labels from row 2

    #get varlabels to do a check on them specifically for key words such as DOB/age/name/address
    varnames = orig_data.columns.tolist()
    varlabels = orig_data.iloc[0].tolist() #headers read already so first row is labels

    #dict to map var names and labels
    df_labels = dict(zip(varnames, varlabels))
    
    #data for pii check:
    df_a  = pd.DataFrame(data_only)
    
     
    ### restrict to rows that have <5 count
    #set threshold for how many occurances the unique value can have via user input
    #keep columns where count of rows is < threshold
    cols_w_lowcounts = df_a.columns[df_a.apply(lambda col: (col.value_counts() < threshold).any())]
    df = df_a[cols_w_lowcounts]

    df_dict = df.to_dict(orient="list")
    
    analyzer = AnalyzerEngine()
    batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
    batch_anonymizer = BatchAnonymizerEngine()
    date_recogniser = get_date_recogniser() 
    analyzer.registry.add_recognizer(date_recogniser) 
    keywordrecogniser = keyword_recogniser()
    analyzer.registry.add_recognizer(keywordrecogniser)

    analyzer_results = batch_analyzer.analyze_dict(df_dict, language="en")
    analyzer_results = list(analyzer_results)
    analyzer_results
    print("Analysing data for PII...")
    
    def parse_recognizer_result(result):
        #parses a result like "type: PERSON, start: 0, end: 11, score: 0.85" and extracts the type if present.
        result_str = str(result)  # ensure the result treated as a string
        match = re.search(r'type:\s*(\w+)', result_str)  #extract type field using regex
        if match:
            return match.group(1) 
        return None

    # initialise dict to store keys and associated types
    key_to_types = defaultdict(set)
    outputs_dict = defaultdict(lambda: defaultdict(list))


    #process the analyzer_results
    for entry in analyzer_results:
        key = entry.key  #extract key
        resultsbyrow = entry.recognizer_results #extract row 
        for rlist in resultsbyrow:
            for r in rlist: #r is recogniserresult object
                score = r.score

        for i, recognizer_result_list in enumerate(resultsbyrow): 
            outputtext = str(df_dict[key][i]) #extract the text that caused a flag  
            vlabels = df_labels.get(key, "") #get var labels from row 2 to include in output
            for result in recognizer_result_list:
            # parse the recogniser result for the 'type'
                flag_type = parse_recognizer_result(result)
                if flag_type:
                    key_to_types[key].add(flag_type)  # use a set to avoid duplicates
                    txtflagged = outputtext[result.start:result.end]  #extract flagged text
                    outputs_dict[key][flag_type].append(txtflagged) 
             
    # convert the aggregated results into dataframe

    ### ignore flag if detecting numeric as person
    #function to find if letters exist in trigger
    def contains_letters(value: str) -> bool:
        return bool(re.search(r"[A-Za-z]", value))    

    
    key_type_list=[]
    
    for key, types in key_to_types.items():
        vlabels = df_labels.get(key, "")
        for t in sorted(types):
            triggers = outputs_dict[key][t]
            #ignore flag if detecting numeric as person
            #filter out false positives for PERSON flag
            filtered_triggers = []
            for trigger in triggers:
                if not contains_letters(trigger) and t == "PERSON":
                    continue         
                filtered_triggers.append(trigger)
            
            if not filtered_triggers:
                continue
            key_type_list.append({
                "variable_name": key,
                "variable_label": vlabels,
                "PII_concern": t,
                "trigger_data": ", ".join(sorted(set(map(str, triggers))))
            })
   
    #still keep df even if rows empty otherwise error if no PII concerns
    if key_type_list:
        key_type_df = pd.DataFrame(key_type_list)
    else:
        key_type_df = pd.DataFrame(columns=["variable_name", "variable_label", "PII_concern", "trigger_data"])
    
    
    #remove flag triggers/entities that are not applicable and might be caugth in error
    key_type_df = key_type_df[~key_type_df["PII_concern"].isin(restrictions)]   

    print("converting results to data frame...")
    print("Saving output file for review...")

    print("File saved. Please review the file to confirm or rule out flags.")
    print("Time taken to run PII checker: ", time.time() - start, "s")
    return key_type_df

