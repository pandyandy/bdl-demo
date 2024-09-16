import streamlit as st
from ui import sidebar_pages

st.title("🎢 Unstructured to Structured Playground")
sidebar_pages()

st.markdown("""
Welcome to the LLM Unstructured to Structured Data Playground! Here, you can experiment with prompting an LLM to convert unstructured data into structured formats.

### How it works:
1. You'll provide an unstructured text input.
2. You'll craft a prompt for the LLM to structure the data.
3. The LLM will attempt to convert the unstructured data based on your prompt.
4. You can iterate and refine your prompts to improve the results.

### Tips for effective prompting:
- Be clear and specific about the desired output format.
- Provide examples if possible.
- Experiment with different prompting techniques.
""")

# User input fields
st.subheader("Tell us about yourself")
name = st.text_input("Your Name")
company = st.text_input("Company Name")
contact = st.text_input("Contact Information")

if name and company and contact:
    st.success(f"Welcome, {name}! Good luck and have fun in the playground!")
    st.page_link('pages/playground.py', label='START', icon='🚀', use_container_width=True)
else:
    st.info("Please fill out all fields to access the playground.")
    st.page_link('pages/playground.py', label='START', icon='🚀', use_container_width=True, disabled=True)