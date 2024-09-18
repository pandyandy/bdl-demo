import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt

from openai import OpenAI
from wordcloud import WordCloud
from ui import sidebar_pages, logo


def analyze_text(text):
    prompt = f"""Analyze the following text and provide:
    1. A list of key entities (people, organizations, locations)
    2. The overall sentiment (positive, negative, or neutral)
    3. A list of main topics
    4. A list of relationships between entities

    Text: {text}

    Respond in the following JSON format:
    {{
        "entities": ["entity1", "entity2", ...],
        "sentiment": "sentiment",
        "topics": ["topic1", "topic2", ...],
        "relationships": [
            {{"entity1": "entity", "entity2": "entity", "relationship": "description"}},
            ...
        ]
    }}
    """


    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.5,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_content = response.choices[0].message.content.strip()

        # Remove backticks and `json` keyword if present
        if raw_content.startswith("```") and raw_content.endswith("```"):
            raw_content = raw_content.strip("```").strip()
        raw_content = raw_content.replace("json", "").strip()

        # Check if the response is empty
        if not raw_content:
            st.error("Received an empty response from the API.")
            return None

        # Attempt to parse JSON
        try:
            analysis = json.loads(raw_content)
            return analysis
        except json.JSONDecodeError:
            st.warning("Received an invalid response format. Please try again. 🙏")
            with st.expander("Response"):
                st.markdown(raw_content)
            return None    
    except Exception as e:
        st.warning(f"An error occurred: {str(e)}")
        return None
        
def create_network_graph(relationships):
    G = nx.Graph()
    for rel in relationships:
        G.add_edge(rel['entity1'], rel['entity2'], relationship=rel['relationship'])
    
    pos = nx.spring_layout(G, k=1.0)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='#B3D6FF', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'), label_pos=0.5)
    plt.title("Entity Relationship Network")
    return plt

def create_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Word Cloud")
    return plt

client = OpenAI(api_key=st.secrets['api_key'])

logo()
st.title("📝 From Unstructured Text to Structured Data")
sidebar_pages()
st.info(
    "Use AI to transform unstructured text data into structured insights. "
    "Enter any text to extract entities, analyze sentiment, identify topics, and visualize relationships.", 
    icon="ℹ️"
    )
text = "Big Data LDN (London) is the UK's leading data, analytics & AI event. The event is a free to attend two-day combined conference and exhibition focusing on how to build dynamic, data-driven enterprises. Delegates will learn from pioneers, experts and real-world case studies, discovering new tools and techniques, enabling them to deliver business value from successful data projects. The event provides delegates with the opportunity to discuss their business requirements with leading technology vendors and consultants and hear from expert speakers in our comprehensive conference programme."
""
text_input = st.text_area("Try with the text below or enter your own:", height=200, value=text)

if st.button("Analyze Text"):
    if text_input:
        with st.spinner("Analyzing text..."):
            analysis = analyze_text(text_input)

            if analysis is not None:
                st.subheader("Entities")    
                st.write(", ".join(analysis['entities']))

                st.subheader("Sentiment")
                st.write(analysis['sentiment'])

                st.subheader("Topics")
                st.write(", ".join(analysis['topics']))

                st.subheader("Relationships")
                for rel in analysis['relationships']:
                    st.write(f"{rel['entity1']} - {rel['relationship']} - {rel['entity2']}")

                st.subheader("Network Graph")
                network_graph = create_network_graph(analysis['relationships'])
                st.pyplot(network_graph)

                st.subheader("Word Cloud")
                word_cloud = create_word_cloud(text_input)
                st.pyplot(word_cloud)

                st.subheader("Structured JSON Output")
                st.json(analysis)