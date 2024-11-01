import streamlit as st
import base64
import os
    
def sidebar_pages():
    with st.sidebar:
        st.page_link('hello.py', label='Home', icon='🏡')
        st.divider()
        st.write("### Examples")
        st.page_link('pages/text.py', label='Text', icon='📝')
        st.page_link('pages/image.py', label='Image', icon='🖼️')
        st.divider()
        st.write("### Try it yourself")
        st.page_link('pages/intro.py', label='Playground', icon='🎢')
        #st.page_link('pages/quest_1.py', label='Challenge 1', icon='🔍')
        #st.page_link('pages/quest_2.py', label='Challenge 2', icon='🔍')
        #st.page_link('pages/quest_3.py', label='Challenge 3', icon='🔍')
        #st.page_link('pages/leaderboard.py', label='Leaderboard', icon='🏆')
        st.divider()
        display_footer_section()

def get_image_base64(image_path: str):
    """Get base64 representation of an image.
    Args:
        image_path (str): Path to the image.
    Returns:
        str: Base64 representation of the image.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def logo():
    LOGO_URL = 'https://assets-global.website-files.com/5e21dc6f4c5acf29c35bb32c/5e21e66410e34945f7f25add_Keboola_logo.svg'

    st.markdown(
        f'''
        <div style="text-align: right;">
            <img src="{LOGO_URL}" alt="Logo" width="150">
        </div>
        ''',
        unsafe_allow_html=True
    )

def display_footer_section():
    # Inject custom CSS for alignment and style
    image_path = os.path.join(os.path.dirname(__file__), 'static/keboola_logo_grey.png')
    logo_base64 = get_image_base64(image_path)
    
    st.markdown(f"""
        <style>
            .footer {{
                width: 100%;
                font-size: 12px;  /* Adjust font size as needed */
                color: #999A9F;  /* Adjust text color as needed */
                padding: 0px 0;  /* Adjust padding as needed */
                display: flex;
                justify-content: left;
                align-items: center;
            }}
            .footer p {{
                margin: 10px 0 10px 0;  /* Removes default margin for p elements */
                padding: 0;  /* Ensures no additional padding is applied */
            }}
            .footer img {{
                height: 20px;  /* Adjust logo size as needed */
                margin-right: 2px; /* Adds spacing between the logo and text */
                margin-left: 3px;
                margin-bottom: 3px;
            }}
            .footer a {{
                color: #999A9F;  /* Change link color */
            }}
        </style>
        <div class="footer">
            <p>
                Powered by
                <img src="data:image/png;base64,{logo_base64}" alt="Logo"> 
                <a href="https://www.keboola.com/">Keboola</a>
            </p>
        </div>
        """, unsafe_allow_html=True)