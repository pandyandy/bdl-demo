import streamlit as st

from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages

st.set_page_config(
    page_title="Keboola AI Playground",
    page_icon="🐙",

)
    
sidebar_pages()
        
LOGO_URL = 'https://assets-global.website-files.com/5e21dc6f4c5acf29c35bb32c/5e21e66410e34945f7f25add_Keboola_logo.svg'

#st.markdown(
#    f'''
#    <div style="text-align: right; margin-bottom: 25px;">
#        <img src="{LOGO_URL}" alt="Logo" width="200">
#    </div>
#    ''',
#    unsafe_allow_html=True
#)
st.header("👋 Welcome to Keboola AI Playground!")
st.markdown("""
    Explore the power of artificial intelligence with Keboola's interactive AI Playground! This app allows you to experience the capabilities of LLMs through a series of engaging quests and challenges.
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([0.7, 0.3])
with col1:
    with stylable_container(key="dark_blue_container", css_styles="{background-color: #004FA3; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""
<h4 style='color: white;'>🤖 What You Can Do</h4>
<p style='color: white;'>
In the Keboola AI Playground, you'll have the opportunity to:
</p>
<ul style='color: white;'>
    <li>Transform unstructured text into structured data</li>
    <li>Ask questions about images and receive AI-generated responses</li>
    <li>Explore other cutting-edge AI capabilities</li>
</ul>
""", unsafe_allow_html=True)
            
col1, col2 = st.columns([0.4, 0.6])
with col2:
    with stylable_container(key="blue_container", css_styles="{background-color: #238DFF; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""  
            <h4 style='color: white;'>🏆 Compete and Learn</h4>
            <p style='color: white;'>As you complete various AI tasks, you'll earn points and climb the leaderboard. Compare your performance with other users and challenge yourself to improve your AI skills.</p>
            """,
                unsafe_allow_html=True
            )
LOGO_URL = 'https://assets-global.website-files.com/5e21dc6f4c5acf29c35bb32c/5e21e66410e34945f7f25add_Keboola_logo.svg'

with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
    with st.container():
        st.markdown(f"""  
#### About Keboola
Keboola is a leader in data integration and analytics platforms. We specialize in helping businesses harness the power of their data through innovative solutions that streamline data processes, from extraction and transformation to analysis and visualization. With Keboola, companies can unlock the full potential of their data assets and drive informed decision-making across their organizations.
""",
unsafe_allow_html=True
)