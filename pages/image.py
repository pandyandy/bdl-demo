import streamlit as st
from openai import OpenAI
from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages

if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'question' not in st.session_state:
    st.session_state.question = None

client = OpenAI(api_key=st.secrets['api_key'])

def ask_openai(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                "type": "image_url",
                "image_url": {
                    "url": "https://innovatek.co.nz/wp-content/uploads/2024/01/Scania_Timber_Truck.jpg",
                },
                },
            ],
            }
        ],
    )
    return response.choices[0].message.content

st.title("Ask Q about an image")

sidebar_pages()

st.image("https://innovatek.co.nz/wp-content/uploads/2024/01/Scania_Timber_Truck.jpg")

col1, col2, col3 = st.columns(3, vertical_alignment="center")
if col1.button("What's in this image?", use_container_width=True):
    question = "What's in this image?"
    answer = ask_openai(question)
    st.session_state.question = question
    st.session_state.answer = answer

if col2.button("How full is the truck?", use_container_width=True):
    question = "How full is the truck?"
    answer = ask_openai(question)
    st.session_state.question = question
    st.session_state.answer = answer

if col3.button("How full is the truck? Answer with a %.", use_container_width=True):
    question = "How full is the truck? Make a qualified guess and answer with a percentage."
    answer = ask_openai(question)
    st.session_state.question = question
    st.session_state.answer = answer

# Text input for custom question
custom_question = st.chat_input("Ask your own question:")
if custom_question:
    answer = ask_openai(custom_question)
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