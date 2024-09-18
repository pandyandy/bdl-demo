import streamlit as st

from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages, logo

st.set_page_config(
    page_title="Keboola AI Playground",
    page_icon="🐙",

)

if 'name' not in st.session_state:
    st.session_state.name = ""
if 'company' not in st.session_state:
    st.session_state.name = ""
if 'contact' not in st.session_state:
    st.session_state.name = ""
    
sidebar_pages()
        
logo()
""
st.header("👋 Welcome to Keboola AI Playground!")
st.markdown("""
    Navigate to the sidebar to explore the following sections:
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([0.7, 0.3])
with col1:
    with stylable_container(key="dark_blue_container", css_styles="{background-color: #004FA3; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""
<h4 style='color: white;'>🧑‍🏫 Examples</h4>
<ul style='color: white;'>
    <li>Discover how to turn unstructured text into clear, structured insights</li>
    <li>Ask questions about images and explore AI-generated answers</li>
</ul>
""", unsafe_allow_html=True)


col1, col2 = st.columns([0.4, 0.6])
with col2:
    with stylable_container(key="blue_container_hello", css_styles="{background-color: #238DFF; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""  
<h4 style='color: white;'>🤓 Try it yourself</h4>
<ul style='color: white;'>
    <li>Dive into the playground, follow a step-by-step guide, and learn how to structure the data on your own</li>
</ul>
""",
    unsafe_allow_html=True
)
st.markdown("#### About Keboola", unsafe_allow_html=True)
with stylable_container(key="grey_container_hello", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: 1em;}"):
    with st.container():
        st.markdown(f"""
Keboola is a data operations platform that empowers organizations to automate their data workflows, integrate various data sources, and create meaningful data products. Our platform is designed to help data engineers, data scientists, and business users collaborate more effectively by simplifying complex data processes and enhancing data-driven decision-making.
""",
unsafe_allow_html=True
)