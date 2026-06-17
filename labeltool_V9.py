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

#add custom recognisers #19/12/25 edit
from custom_date_recogniser import get_date_recogniser 
from custom_varlabel_recogniser import keyword_recogniser 


#track time taken for tool to run
start = time.time()

def userinput(combined_data, threshold, restrictions):
    #data
    orig_data = combined_data #getting this from combine_data_metadata.py so data has var labels in 2nd row
    print("Data loaded.")
 
    data_only = orig_data.iloc[1:].reset_index(drop=True) #varnames and data only, ignore labels from row 2
    
    #get varlabels to do a check on them specifically for key words such as DOB/age/name/address
    varnames = orig_data.columns.tolist()
    varlabels = orig_data.iloc[0].tolist() #headers read already so first row is labels
    
    #dict to map var names and labels
    df_labels = dict(zip(varnames, varlabels))
    df_dict = df_labels
        
    #convert metadata to dataframe for pii check:
    df_labels_df = pd.DataFrame(list(df_labels.items()),columns=["variable","label"])
    df_l = df_labels_df 

    analyzer = AnalyzerEngine()
    keywordrecogniser = keyword_recogniser()

    analyzer.registry.add_recognizer(keywordrecogniser)
    batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
    analyzer_results = batch_analyzer.analyze_dict(df_labels, language="en")
    analyzer_results = list(analyzer_results)
    analyzer_results
    
    results_list = []
    print("Analysing variable labels for PII risk...")
    for _, row in df_l.iterrows():
        var=row["variable"]
        label = str(row["label"])
        
        results = analyzer.analyze(text = label,language = "en")
        for res in results:
            results_list.append({
                "variable": var,
                "label": label,
                "PII_concern": res.entity_type
            })
    
    #still keep df even if rows empty
    if results_list:
        results_df = pd.DataFrame(results_list)
    else:
        results_df = pd.DataFrame(columns=["variable","label","PII_concern"])
    
    #ignore general PII flags and include custom keywords
    ignorelist = ['DOB_DOD_CUSTOM', 'CRYPTO', 'US_PASSPORT', 'DATE_TIME', 'US_BANK_NUMBER', 'UK_NHS', 'NRP', 'US_ITIN', 'MEDICAL_LICENSE', 'US_SSN', 'IP_ADDRESS', 'IBAN_CODE', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 'LOCATION', 'CREDIT_CARD', 'US_DRIVER_LICENSE', 'URL', 'PERSON', 'MAC_ADDRESS','US_MBI','UK_NINO','UK_POSTCODE','UK_VEHICLE_REGISTRATION','ES_NIF','ES_NIE','IT_FISAL_CODE','IT_DRIVER_LICENSE','IT_VAT_CODE','IT_PASSPORT','IT_IDENTITY_CARD','PL_PESEL','SG_NRIC_FIN','SG_UEN','AU_ABN','AU_ACN','AU_TFN','AU_MEDICARE','IN_PAN','IN_ADDHAAR','IN_VEHICLE_REGISTRATION','IN_VOTER','IN_PASSPORT','IN_GSTIN','FI_PERSONAL_IDENTITY_CODE','KR_DRIVER_LICENSE','KR_FRN','KR_PASSPORT','KR_BRN','KR_RRN','NG_NIN','NG_VEHICLE_REGISTRATION','TH_TNIN']
    narrowed_results_df = results_df[~results_df["PII_concern"].isin(ignorelist)]   

    return narrowed_results_df 
   
    return label_flags
