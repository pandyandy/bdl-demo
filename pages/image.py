import streamlit as st
from openai import OpenAI
from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages, logo
import requests
from PIL import Image
from io import BytesIO

if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'question' not in st.session_state:
    st.session_state.question = None
if 'answer_custom' not in st.session_state:
    st.session_state.answer_custom = None
if 'question_custom' not in st.session_state:
    st.session_state.question_custom = None
if 'url' not in st.session_state:
    st.session_state.url = None
if '_url' not in st.session_state:
    st.session_state._url = st.session_state.url

client = OpenAI(api_key=st.secrets['api_key'])

def ask_openai(question, image_url):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions about images. If the question is not related to the image, don't answer."},
            {"role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
                },
            ],
            }
        ],
    )
    return response.choices[0].message.content

def update_url():
    """
    Updates the number of input questions.
    """
    st.session_state.url = st.session_state._url

def is_valid_image_url(url):
    try:
        response = requests.get(url)
        # Check if response status code is OK (200) and content-type is an image
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

logo()
st.title("🖼️ Ask Questions About an Image")
st.info(
    "Use AI to ask questions about images. You can work with an existing image or provide your own image URL.",
    icon="ℹ️"
    )

sidebar_pages()
""
image_option = st.radio("Choose an image source:", ("Use Predefined Image", "Enter Custom URL"), horizontal=True, label_visibility='collapsed')

if image_option == "Use Predefined Image":
    image_url = "https://innovatek.co.nz/wp-content/uploads/2024/01/Scania_Timber_Truck.jpg"
    st.image(image_url)
    
    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.3, 0.2], vertical_alignment="center")
    if col1.button("What's in this image?", use_container_width=True):
        question = "What's in this image?"
        answer = ask_openai(question, image_url)
        st.session_state.question = question
        st.session_state.answer = answer

    if col2.button("How full is the truck?", use_container_width=True):
        question = "How full is the truck?"
        answer = ask_openai(question, image_url)
        st.session_state.question = question
        st.session_state.answer = answer

    if col3.button("How full is the truck? Answer with a %.", use_container_width=True):
        question = "How full is the truck? Make a qualified guess and return only the percentage as an answer."
        answer = ask_openai(question, image_url)
        st.session_state.question = "How full is the truck? Answer with a percentage."
        st.session_state.answer = answer

    if col4.button("JSON Format Response", use_container_width=True):
        question = """
        Analyze the image and answer:
        1. What's in the image?
        2. How full is the truck? Make a qualified guess and return only the percentage as an answer.

        Respond in the following JSON format:
        {{
            "object": "object",
            "estimated_fullness_percentage": "75"
        }}
        """
        answer = ask_openai(question, image_url)
        st.session_state.question = "Describe the image and estimate the fullness of the truck. Respond in JSON format."
        st.session_state.answer = answer

        # Text input for custom question
    custom_question = st.chat_input("Ask your own question:")
    if custom_question:
        answer = ask_openai(custom_question, image_url)
        st.session_state.question = custom_question
        st.session_state.answer = answer

    if st.session_state.answer:
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col2:
            with st.container():
                st.markdown(f"{st.session_state.answer}")
        with col1:
            st.write("🤖")

elif image_option == "Enter Custom URL":
    st.session_state.url = st.session_state._url
    image_url = st.text_input("Enter the URL of the image you'd like to analyze:", key='_url', on_change=update_url)

    if image_url:
        if is_valid_image_url(image_url):
            st.image(image_url)
        else:
            st.warning("Invalid image URL. Please provide a valid URL pointing to an image.")

    # Text input for custom question
    custom_question = st.chat_input("Ask your own question:")
    if custom_question:
        answer = ask_openai(custom_question, image_url)
        st.session_state.question_custom = custom_question
        st.session_state.answer_custom = answer

    if st.session_state.answer_custom is not None:
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question_custom}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col2:
            with st.container():
                st.markdown(f"{st.session_state.answer_custom}")
        with col1:
            st.write("🤖")