# client.py

import streamlit as st
#from keboola_streamlit import KeboolaStreamlit
from pages.kstr import KeboolaStreamlit


def get_keboola_client():
    """
    This function retrieves the necessary credentials from the Streamlit secrets and uses them to create
    a KeboolaStreamlit object.
    
    Returns: 
        KeboolaStreamlit object
    """
    URL = st.secrets["KEBOOLA_URL"]
    TOKEN = st.secrets["STORAGE_API_TOKEN"] 
    return KeboolaStreamlit(URL, TOKEN)

keboola = get_keboola_client()