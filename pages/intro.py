import streamlit as st
from ui import sidebar_pages, logo

if 'name' not in st.session_state:
    st.session_state.name = None
if 'company' not in st.session_state:
    st.session_state.company = None
if 'contact' not in st.session_state:
    st.session_state.contact = None
if '_name' not in st.session_state:
    st.session_state._name =  st.session_state.name
if '_company' not in st.session_state:
    st.session_state._company = st.session_state.company
if '_contact' not in st.session_state:
    st.session_state._contact = st.session_state.contact

def update_name():
    """
    Updates the number of input questions.
    """
    st.session_state.name = st.session_state._name


def update_company():
    """
    Updates the number of input questions.
    """
    st.session_state.company = st.session_state._company


def update_contact():
    """
    Updates the number of input questions.
    """
    st.session_state.contact = st.session_state._contact

logo()
st.title("🎢 Unstructured to Structured Playground")
sidebar_pages()

st.markdown("""
Welcome to the Playground! Here, you can experiment with prompting an LLM to convert unstructured data into structured insights. 

### How it works:
1. Choose from different unstructured text inputs or provide your own.
2. Go through a few steps of prompting to structure the data.
3. The LLM will attempt to convert the unstructured data based on your prompt.
4. You can iterate and refine your prompts to improve the results.

### Tips for effective prompting:
- Be clear and specific about the desired output format.
- Provide examples if possible.
- Experiment with different prompting techniques.
""")

# User input fields
st.subheader("Tell us about yourself")
st.session_state._name = st.session_state.name
st.text_input("Your Name", key='_name', on_change=update_name)
st.session_state._company = st.session_state.company
st.text_input("Company Name", key='_company', on_change=update_company)
st.session_state._contact = st.session_state.contact
st.text_input("Contact Information", key='_contact', on_change=update_contact)

if st.session_state.name and st.session_state.company and st.session_state.contact:
    st.success(f"Welcome, {st.session_state.name}! Good luck and have fun in the playground! 🐙")
    st.page_link('pages/playground.py', label='START', icon='🚀', use_container_width=True)
else:
    st.info("Please fill out all fields to access the playground.")
    st.page_link('pages/playground.py', label='START', icon='🚀', use_container_width=True, disabled=True)