# Elen Golightly November 2025
# App to have a streamlit UI for PII checker

import streamlit as st
import labeltool_V9 #does keyword check of variable labels
import datatool_V9 #does pii check of data
import combine_data_metadata_V2
from PIL import Image

#add logo
logo = Image.open("serplogo.png")
st.image(logo, width=200)

#developer note
st.markdown("*Initial development by Elen Golightly 2025*")

st.title("PII Check")
input_file = st.file_uploader("Select csv data file.")
metadata_file = st.file_uploader("Select xlsx metadata file")


threshold = st.number_input("Threshold for number of unique values", min_value=1, value=5)
#allow user to ignore certain flags within checks:
restrictions = st.multiselect("Restrictions (flags you don't want to search for)", ['DOB_DOD_CUSTOM', 'CRYPTO', 'US_PASSPORT', 'DATE_TIME', 'US_BANK_NUMBER', 'UK_NHS', 'NRP', 'US_ITIN', 'MEDICAL_LICENSE', 'US_SSN', 'IP_ADDRESS', 'IBAN_CODE', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 'LOCATION', 'CREDIT_CARD', 'US_DRIVER_LICENSE', 'URL', 'PERSON', 'MAC_ADDRESS','US_MBI','UK_NINO','UK_POSTCODE','UK_VEHICLE_REGISTRATION','ES_NIF','ES_NIE','IT_FISAL_CODE','IT_DRIVER_LICENSE','IT_VAT_CODE','IT_PASSPORT','IT_IDENTITY_CARD','PL_PESEL','SG_NRIC_FIN','SG_UEN','AU_ABN','AU_ACN','AU_TFN','AU_MEDICARE','IN_PAN','IN_ADDHAAR','IN_VEHICLE_REGISTRATION','IN_VOTER','IN_PASSPORT','IN_GSTIN','FI_PERSONAL_IDENTITY_CODE','KR_DRIVER_LICENSE','KR_FRN','KR_PASSPORT','KR_BRN','KR_RRN','NG_NIN','NG_VEHICLE_REGISTRATION','TH_TNIN'])

#to allow double download button without one dissapearing after click
if "ran" not in st.session_state:
    st.session_state.ran = False
if "file1" not in st.session_state:
    st.session_state.file1 = None
if "file2" not in st.session_state:
    st.session_state.file2 = None


if st.button("Run"):
    if input_file is not None and metadata_file is not None:
        # get combined data and metadata
        combined_data = combine_data_metadata_V2.userinput(input_file, metadata_file)
        # run PII tool
        output_label_check = labeltool_V9.userinput(combined_data, threshold, restrictions)
        output_data_check = datatool_V9.userinput(combined_data, threshold, restrictions)
        st.success(f"Done! Please carry out a secondary review of the flags in your output files.")   
              
        #convert dataframes to bytes for download
        st.session_state.file1 = output_label_check.to_csv(index=False)
        st.session_state.file2 = output_data_check.to_csv(index=False)
        #mark that it's run
        st.session_state.ran = True
       
    else:
        st.error("Please upload file first.")


#download files buttons
if st.session_state.ran: 
    st.download_button(
        label = "Download flagged variables from metadata.",
        data = st.session_state.file1,
        file_name = "Flagged_variables_from_labels.csv",
        mime="text/csv"
    )
    st.download_button(
        label = "Download flagged variables from dataset.",
        data = st.session_state.file2,
        file_name = "Flagged_variables_from_data.csv",
        mime="text/csv"
       )