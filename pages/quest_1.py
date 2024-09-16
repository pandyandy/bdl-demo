import streamlit as st
import json 

from openai import OpenAI
from streamlit_extras.stylable_container import stylable_container
from difflib import SequenceMatcher 

st.page_link('pages/start.py', label='Go back', icon='↩️')
    
st.title("Challenge 1: The Ultimate Prompt")
st.info("In this challenge, your task is to write a prompt that will instruct the AI model to extract entities, analyze sentiment, identify topics, and relationships from the text below. Desired output format is JSON.", icon="ℹ️")
st.write("The text you're working with:")
text = ("Big Data LDN (London) is the UK's leading data, analytics & AI event. "
        "The event is a free to attend two-day combined conference and exhibition focusing on how to build dynamic, data-driven enterprises. "
        "Delegates will learn from pioneers, experts and real-world case studies, discovering new tools and techniques, enabling them to deliver business value from successful data projects. "
        "The event provides delegates with the opportunity to discuss their business requirements with leading technology vendors and consultants and hear from expert speakers in our comprehensive conference programme.")

with stylable_container(key="blue_container", css_styles="{background-color: #238DFF; border-radius: 0.5rem; padding: 1em;}"):
    with st.container():
        st.markdown(f"""
        <p style='color: white;'>{text}</p>
        """,
            unsafe_allow_html=True
        )
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

st.session_state.prompt = st.text_area("Write your prompt here:")

st.caption("_The text will be appended at the end of the prompt in the following format: Text: {text}_")

client = OpenAI(api_key=st.secrets['api_key'])

def analyze_text(text, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.5,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prompt}\n\nText: {text}"}
            ]
        )
        raw_content = response.choices[0].message.content.strip()

        # Remove backticks and `json` keyword if present
        #if raw_content.startswith("```") and raw_content.endswith("```"):
        #    raw_content = raw_content.strip("```").strip()
        #raw_content = raw_content.replace("json", "").strip()

        # Check if the response is empty
        #if not raw_content:
        #    st.error("Received an empty response from the API.")
        #    return None

        # Attempt to parse JSON
        #analysis = json.loads(raw_content)
        return raw_content #analysis
    #except json.JSONDecodeError:
     #   st.error("Failed to decode JSON. The API response might be invalid.")
      #  st.warning("Invalid JSON Response:", raw_content)  # Debug: Print the problematic response
       # return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
    

def compare_responses(user_response, ideal_response):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.5,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"""
                 Compare the user response with the ideal response and provide a similarity score in percentage.\n\nUser Response: {user_response}\n\nIdeal Response: {ideal_response}.\n\nReturn just the number as response, nothing else.
        """}
            ]
        )
        raw_content = response.choices[0].message.content.strip()

        # Remove backticks and `json` keyword if present
        #if raw_content.startswith("```") and raw_content.endswith("```"):
        #    raw_content = raw_content.strip("```").strip()
        #raw_content = raw_content.replace("json", "").strip()

        # Check if the response is empty
        #if not raw_content:
        #    st.error("Received an empty response from the API.")
        #    return None

        # Attempt to parse JSON
        #analysis = json.loads(raw_content)
        return raw_content #analysis
    #except json.JSONDecodeError:
     #   st.error("Failed to decode JSON. The API response might be invalid.")
      #  st.warning("Invalid JSON Response:", raw_content)  # Debug: Print the problematic response
       # return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if st.button("Submit"):

    st.session_state.analysis = analyze_text(text, st.session_state.prompt)
    if st.session_state.analysis:
        st.write("Here's the response from the AI model:")
        st.write(st.session_state.analysis)
        #st.json(analysis)


if 'analysis' in st.session_state and st.session_state.analysis:
    if st.button("Compare"):
        # Ideal JSON response for comparison
        json_response = {
            "entities": [
                "Big Data LDN",
                "UK",
                "London",
                "delegates",
                "technology vendors",
                "consultants",
                "expert speakers"
            ],
            "sentiment": "positive",
            "topics": [
                "data",
                "analytics",
                "AI",
                "conference",
                "exhibition",
                "data-driven enterprises",
                "business value",
                "data projects"
            ],
            "relationships": [
                {"entity1": "Big Data LDN", "entity2": "UK", "relationship": "located in"},
                {"entity1": "Big Data LDN", "entity2": "London", "relationship": "hosted in"},
                {"entity1": "delegates", "entity2": "Big Data LDN", "relationship": "attend"},
                {"entity1": "delegates", "entity2": "technology vendors", "relationship": "discuss business requirements with"},
                {"entity1": "delegates", "entity2": "consultants", "relationship": "discuss business requirements with"},
                {"entity1": "expert speakers", "entity2": "conference programme", "relationship": "participate in"}
            ]
        }
        
        # Calculate similarity score
        similarity_score = compare_responses(st.session_state.analysis, json_response)
        st.write(f"Similarity score with the ideal response: {similarity_score}%")