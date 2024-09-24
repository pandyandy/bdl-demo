import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import pandas as pd
from datetime import datetime

from openai import OpenAI
from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages, logo
from pages.client import keboola

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'question_step_2' not in st.session_state:
    st.session_state.question_step_2 = ""
if '_question_step_2' not in st.session_state:
    st.session_state._question_step_2 = st.session_state.question_step_2
if 'llm_response_step_2' not in st.session_state:
    st.session_state.llm_response_step_2 = ""
if 'question_step_3' not in st.session_state:
    st.session_state.question_step_3 = ""
if '_question_step_3' not in st.session_state:
    st.session_state._question_step_3 = st.session_state.question_step_3
if 'llm_response_step_3' not in st.session_state:
    st.session_state.llm_response_step_3 = ""
if 'question_step_4' not in st.session_state:
    st.session_state.question_step_4 = ""
if '_question_step_4' not in st.session_state:
    st.session_state._question_step_4 = st.session_state.question_step_4
if 'llm_response_step_4' not in st.session_state:
    st.session_state.llm_response_step_4 = ""
if 'question_step_5' not in st.session_state:
    st.session_state.question_step_5 = ""
if '_question_step_5' not in st.session_state:
    st.session_state._question_step_5 = st.session_state.question_step_5
if 'llm_response_step_5' not in st.session_state:
    st.session_state.llm_response_step_5 = ""
if 'llm_response_step_4_json' not in st.session_state:
    st.session_state.llm_response_step_4_json = None
if 'llm_response_step_5_json' not in st.session_state:
    st.session_state.llm_response_step_5_json = None
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'name' not in st.session_state:
    st.session_state.name = None
if 'company' not in st.session_state:
    st.session_state.name = None
if 'contact' not in st.session_state:
    st.session_state.name = None
    
logo()
st.header("🎢 Unstructured to Structured Data Playground")
sidebar_pages()

def sidebar_text(text):
    st.sidebar.divider()
    st.sidebar.write("**Selected Text:**")
    with st.sidebar.container(border=True):
        st.markdown(text, unsafe_allow_html=True)


client = OpenAI(api_key=st.secrets['api_key'])

def update_question_step_2():
    """
    Updates the number of input questions.
    """
    st.session_state.question_step_2 = st.session_state._question_step_2

def update_question_step_3():
    """
    Updates the number of input questions.
    """
    st.session_state.question_step_3 = st.session_state._question_step_3

def update_question_step_4():
    """
    Updates the number of input questions.
    """
    st.session_state.question_step_4 = st.session_state._question_step_4

def update_question_step_5():
    """
    Updates the number of input questions.
    """
    st.session_state.question_step_5 = st.session_state._question_step_5


def get_llm_response(user_prompt):
    try:
        with st.spinner("🤖 Processing your request... please wait!"):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0 
            )
            response = response.choices[0].message.content
            return response.strip()
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def buttons():
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1], vertical_alignment='center')
    if col1.button("⏪", on_click=lambda: st.session_state.update(step=st.session_state.step - 1), use_container_width=True):
        st.rerun()
    if col3.button("⏩", on_click=lambda: st.session_state.update(step=st.session_state.step + 1), use_container_width=True):
        st.rerun()

# Step 1: User chooses text
def step1():
    st.write("### Step 1: Choose Your Text")
    st.markdown("Start by selecting a text type. This will be the basis for our analysis in the following steps.")
    
    choice = st.radio("Choose your input type:", options=["Article", "Review", "Social media post", "Your own text"])
    source = None
    if choice == "Social media post":
        text_input = """Big Data LDN - 18/19 Sept 24<br>@BigData_LDN<br><br>ICYMI, our Headline Keynote Panel this year features not one, not two... but THREE Olympic Gold medallists!<br>Learn about the relationship between #data and elite sporting performance with this amazing line-up, at the Y Axis Keynote and streamed live to ALL our theatres.<br>Register FREE now: https://bit.ly/4ejzXNI"""
        source = "https://x.com/BigData_LDN/status/1834155044880420870"
    elif choice == "Review":
        text_input = """This was a great event with so many networking opportunities. We had the chance to listen to some brilliant speakers. I would highly recommend it. The event involved a wide range of talks on various subjects within analytics and AI."""
        source = "https://www.eventible.com/it/big-data-ldn"
    elif choice == "Article":
        text_input = "Big Data LDN (London) is the UK's leading data, analytics & AI event.<br><br>The event is a free to attend two-day combined conference and exhibition focusing on how to build a dynamic, data-driven business.<br><br>Attendees will learn from expert data leaders and data success stories from some of the world's most recognisable brands. This in turn allows them to discover new tools and techniques that enable them to deliver business value from successful data projects.<br><br>The event provides the data community with the opportunity to discuss their business requirements with leading technology vendors and consultants whilst hearing from expert speakers in our comprehensive conference programme."
        source = "https://www.bigdataldn.com/en-gb/help/faqs.html"
    else:
        text_input = st.text_area("Enter your own text:", value="", height=200)
    
    st.write("**Selected Text:**")
    with stylable_container(key="blue_container", css_styles="{background-color: #f2f8ff; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""
                {text_input}
                 """, unsafe_allow_html=True)
    
    if source:
        st.caption(f"[Source]({source})")
    
    st.session_state.df = pd.DataFrame({
        'name': [st.session_state.name],
        'company': [st.session_state.company],
        'contact': [st.session_state.contact],
        'date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })

    keboola.write_table(table_id='in.c-bdl.data-app-bdl', df=st.session_state.df, is_incremental=True)

    col1, col2, col3 = st.columns(3)
    if col3.button("⏩ Continue to Step 2", on_click=lambda: st.session_state.update(step=st.session_state.step + 1, text_input=text_input), use_container_width=True):
        st.rerun()

# Step 2: Initial analysis
def step2():
    buttons()
    sidebar_text(st.session_state.text_input)
    st.write("### Step 2: Initial Text Analysis")
    st.markdown("Now that you've selected your text, let's perform an initial analysis! Instruct the LLM to identify key elements such as entities, main topics, keywords, or target audience.")
    with st.expander("**💡 Hint**"):
        prompt = """Analyze the following text and provide:
        1. A list of key entities (people, organizations, locations)
        2. A list of main topics
        3. A list of important keywords
        4. A list of the types of audience the text is addressing"""

        st.caption(f"""Experiment with various prompts to explore different results. For example, an initial discovery prompt could be:
        
        {prompt}
        
        """)
        st.caption("You can also try requesting responses in different formats, such as lists or dictionaries.")
        col1, col2, col3 = st.columns(3)
        if col3.button("Try it!", use_container_width=True):
            st.session_state.llm_response_step_2 = get_llm_response(f"Instruction: {prompt}\nText: {st.session_state.text_input}")
            st.session_state.question_step_2 = prompt
    
    "" 
    st.session_state._question_step_2 = st.session_state.question_step_2
    user_prompt = st.text_area("Write your prompt here:", key='_question_step_2', on_change=update_question_step_2, height=150)
    col1, col2, col3, col4 = st.columns(4)
    if col4.button("Submit", use_container_width=True):
        st.session_state.llm_response_step_2 = get_llm_response(f"Instruction: {user_prompt}\nText: {st.session_state.text_input}")
        
    if st.session_state.llm_response_step_2:
        ""
        with st.container(border=True):
            try:
                response_json = json.loads(st.session_state.llm_response_step_2)
                st.json(response_json)
            except json.JSONDecodeError:
                st.markdown(st.session_state.llm_response_step_2)
                    
# New function for sentiment analysis step
def step3():
    buttons()
    sidebar_text(st.session_state.text_input)
    st.write("### Step 3: Sentiment Analysis")
    st.markdown("Try instructing the LLM to perform a sentiment analysis on the text. In your prompt, ask for the sentiment to be quantified on a scale from -1 (highly negative) to 1 (highly positive), following the example provided in the presentation.")
    with st.expander("**💡 Hint**"):
        prompt = """Using a scale from -1 (highly negative) to 1 (highly positive), perform a sentiment analysis on the following text and return only the sentiment score as a response."""    
        prompt_to_display = """Using a scale from -1 (highly negative) to 1 (highly positive), 
    perform a sentiment analysis on the following text and return only
    the sentiment score as a response."""        
       
        st.caption(f"""When asking for a sentiment analysis, you might want the output to include only the sentiment score. Experiment with phrasing your prompts to ensure the LLM provides just the number. For example:
        
        {prompt_to_display}
        
        """)

        col1, col2, col3 = st.columns(3)
        if col3.button("Try it!", use_container_width=True):
            st.session_state.llm_response_step_3 = get_llm_response(f"Instruction: {prompt}\nText: {st.session_state.text_input}")
            st.session_state.question_step_3 = prompt

    "" 
    st.session_state._question_step_3 = st.session_state.question_step_3
    user_prompt = st.text_area("Write your prompt here:", key='_question_step_3', on_change=update_question_step_3, height=150)
    col1, col2, col3, col4 = st.columns(4)
    if col4.button("Submit", use_container_width=True):
        st.session_state.llm_response_step_3 = get_llm_response(f"Instruction: {user_prompt}\nText: {st.session_state.text_input}")
        st.session_state.question_step_3 = user_prompt
    
    if st.session_state.llm_response_step_3:
        ""
        with st.container(border=True):
            st.markdown(f"{st.session_state.llm_response_step_3}")


# Step 4: Create structured data
def step4():
    buttons()
    sidebar_text(st.session_state.text_input)
    st.write("### Step 4: Create Structured Data")
    st.markdown("Don't worry if the results from previous steps aren't perfectly structured. That's our goal now! To achieve it, instruct the LLM to convert the extracted key elements and sentiment score into a structured JSON format.")
    with st.expander("**💡 Hint**"):
        prompt = """You are given information that has been extracted from previous analyses. Your task is to structure it properly. Respond in the following JSON format:
{
    "entities": ["entity1", "entity2", ...],
    "sentiment": "sentiment",
    "topics": ["topic1", "topic2", ...],
        ...
}"""
        prompt_to_display = """
            You are given information that has been extracted from previous analyses.
            Your task is to structure it properly. Respond in the following JSON format:
            {
                "entities": ["entity1", "entity2", ...],
                "sentiment": "sentiment",
                "topics": ["topic1", "topic2", ...],
                    ...
            }
        """
        st.caption(f"""
        If the JSON output isn't as expected, consider refining your prompt. You can explicitly specify the desired format, such as:
        {prompt_to_display}
        """)
        col1, col2, col3 = st.columns(3)
        if col3.button("Try it!", use_container_width=True):
            st.session_state.llm_response_step_4 = get_llm_response(f"Instruction: {prompt}\nKey Elements: {st.session_state.llm_response_step_2}\nSentiment: {st.session_state.llm_response_step_3}")
            st.session_state.question_step_4 = prompt

    ""
    st.session_state._question_step_4 = st.session_state.question_step_4
    user_prompt = st.text_area("Write your prompt here:", key='_question_step_4', on_change=update_question_step_4, height=150)
    col1, col2, col3, col4 = st.columns(4)
    if col4.button("Submit", use_container_width=True):
        st.session_state.llm_response_step_4 = get_llm_response(f"Instruction: {user_prompt}\nKey Elements: {st.session_state.llm_response_step_2}\nSentiment: {st.session_state.llm_response_step_3}")
        st.session_state.question_step_4 = user_prompt
    
    if st.session_state.llm_response_step_4:
        ""
        with st.container(border=True):
            try:
                json_response = json.loads(st.session_state.llm_response_step_4)
                st.json(json_response)  # If it is valid JSON, display it as JSON
                st.session_state.llm_response_step_4_json = json_response
            except (ValueError, TypeError):
                st.markdown(st.session_state.llm_response_step_4)
                st.session_state.llm_response_step_4_json = None
    
    if st.session_state.llm_response_step_2:
        ""
        with st.expander("Previous Results"):
            st.write("**Extracted Key Elements from Initial Analysis:**")
            st.markdown(f"{st.session_state.llm_response_step_2}")
            if st.session_state.llm_response_step_3:
                st.write("**Sentiment Analysis Results:**")
                st.markdown(f"{st.session_state.llm_response_step_3}")

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

# Step 5: Generate visualizations
def step5():
    buttons()
    sidebar_text(st.session_state.text_input)
    st.write("### Step 5: Visualize Relationships")

    st.markdown("Let's identify relationships between entities in the text to create a visual network graph! The expected outcome here should include: 'entity1', 'entity2', and 'relationship' fields.")
         
    
    with st.expander("**💡 Hint**"):
        prompt = f"""Analyze the following text and provide a list of relationships between entities. Respond in the following JSON format:
    {{
        "relationships": [
            {{"entity1": "entity", "entity2": "entity", "relationship": "description"}},
            ...
        ]
    }}"""
        prompt_to_display = f"""
            Analyze the following text and provide a list of relationships between entities. 
            Respond in the following JSON format:
            {{
                "relationships": [
                    {{"entity1": "entity", "entity2": "entity", "relationship": "description"}},
                    ...
                ]
            }}
        """
        st.caption(f"""
        To ensure the output is structured correctly, you can use a prompt like this:
        {prompt_to_display}
        By specifying this format, you'll receive a structured output, making it easy to generate a visual network graph based on the relationships identified.
        """)
        col1, col2, col3 = st.columns(3)
        if col3.button("Try it!", use_container_width=True):
            st.session_state.llm_response_step_5 = get_llm_response(f"Instruction: {prompt}\nText: {st.session_state.text_input}")
            st.session_state.question_step_5 = prompt
    ""
    st.session_state._question_step_5 = st.session_state.question_step_5
    user_prompt = st.text_area("Write your prompt here:", key='_question_step_5', height=150, on_change=update_question_step_5)
    col1, col2, col3, col4 = st.columns(4)
    if col4.button("Submit", use_container_width=True):
        st.session_state.llm_response_step_5 = get_llm_response(f"Instruction: {user_prompt}\nText: {st.session_state.text_input}")
        st.session_state.question_step_5 = user_prompt
    
    if st.session_state.llm_response_step_5:
        ""
        with st.container(border=True):
            raw_content = st.session_state.llm_response_step_5
            try:
                analysis = json.loads(raw_content)
                st.json(analysis)
                st.session_state.llm_response_step_5_json = analysis

                # Ensure the response contains the 'relationships' key
                if 'relationships' in analysis:
                    network_graph = create_network_graph(analysis['relationships'])
                    st.pyplot(network_graph)
                else:
                    st.info("Cannot create a network graph. The response does not contain the expected 'relationships' field.", icon='ℹ️')
            
            except json.JSONDecodeError:
                # If JSON parsing fails, handle code blocks or other formats
                if raw_content.startswith("```") and raw_content.endswith("```"):
                    raw_content = raw_content.strip("```").strip()
                raw_content = raw_content.replace("json", "").strip()

                try:
                    analysis = json.loads(raw_content)
                    st.json(analysis)
                    st.session_state.llm_response_step_5_json = analysis
                    
                    if 'relationships' in analysis:
                        network_graph = create_network_graph(analysis['relationships'])
                        st.pyplot(network_graph)
                    else:
                        st.info("Cannot create a network graph. The response does not contain the expected 'relationships' field.")
            
                except json.JSONDecodeError:
                    st.markdown(raw_content)
                    st.session_state.llm_response_step_5_json = None
                    st.info("Cannot create a network graph. The response is not in the expected JSON format. Please check out the hint for more information on the required structure.", icon='ℹ️')

# Step 6: Create an interactive summary
def step6():
    col1, col2, col3 = st.columns([0.1, 0.6, 0.3], vertical_alignment='center')
    if col1.button("⏪", on_click=lambda: st.session_state.update(step=st.session_state.step - 1), use_container_width=True):
        st.rerun()
    if col3.button("🔁 Start Again", on_click=lambda: st.session_state.update(
        step=1,
        question_step_2="",
        llm_response_step_2="",
        question_step_3="",
        llm_response_step_3="",
        question_step_4="",
        llm_response_step_4="",
        question_step_5="",
        llm_response_step_5="",
        llm_response_step_4_json=None,
        llm_response_step_5_json=None), 
        use_container_width=True):
        st.rerun()

    st.write("### Step 6: Final Report")
    st.success("Congratulations! You've completed all steps. 🎉")
    ""
    st.markdown("#####  Here's the final output of your analysis:", unsafe_allow_html=True)
    ""
    st.write("**📑 From unstructured text input...**")
    with stylable_container(key="blue_container", css_styles="{background-color: #f2f8ff; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"{st.session_state.text_input}", unsafe_allow_html=True)
    
    response_step_4_json = st.session_state.llm_response_step_4_json
    response_step_5_json = st.session_state.llm_response_step_5_json

    if response_step_4_json is None and response_step_5_json is None:
        output_json = None
    elif response_step_4_json is None:
        output_json = response_step_5_json
    elif response_step_5_json is None:
        output_json = response_step_4_json
    else:
        output_json = {**response_step_4_json, **response_step_5_json}
    ""
    st.write("**💡 To structured insights:**")
    if output_json:
        st.json(output_json)
        ""
        st.write("**📈 And their visualization:**")
        if 'relationships' in output_json:
            network_graph = create_network_graph(output_json['relationships'])
            st.pyplot(network_graph)
        else:
            st.info("Cannot create a network graph. The response does not contain the expected 'relationships' field.", icon='ℹ️')
    else:
        st.warning("It seems like no structured data was generated. 😢 You can start again by hitting the button above.")

# Main game loop
if st.session_state.step == 1:
    step1()
elif st.session_state.step == 2:
    step2()
elif st.session_state.step == 3:
    step3()
elif st.session_state.step == 4:
    step4()
elif st.session_state.step == 5:
    step5()
elif st.session_state.step == 6:
    step6()

