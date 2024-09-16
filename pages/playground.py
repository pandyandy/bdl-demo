import streamlit as st
from openai import OpenAI
import os
import networkx as nx
import matplotlib.pyplot as plt
import time
from streamlit_extras.stylable_container import stylable_container
from ui import sidebar_pages
import json

# Set your OpenAI API Key
#openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=st.secrets['api_key'])
# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'llm_response' not in st.session_state:
    st.session_state.llm_response = ""
if 'llm_response_step_2' not in st.session_state:
    st.session_state.llm_response_step_2 = ""
if 'llm_response_step_3' not in st.session_state:
    st.session_state.llm_response_step_3 = ""
if 'llm_response_step_4' not in st.session_state:
    st.session_state.llm_response_step_4 = ""
if 'llm_response_step_5' not in st.session_state:
    st.session_state.llm_response_step_5 = ""
if 'llm_response_sentiment' not in st.session_state:
    st.session_state.llm_response_sentiment = ""
if 'summary_response' not in st.session_state:
    st.session_state.summary_response = ""
if 'insights_response' not in st.session_state:
    st.session_state.insights_response = ""


st.title("🎢 Unstructured to Structured Playground")
sidebar_pages()
# The text we will work with across all levels
# Function to make API call to GPT model
def get_llm_response(user_prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0  # For deterministic output
    )
    response = response.choices[0].message.content
    return response.strip()

# Step 1: User chooses text
def step1():
    st.write("### Step 1: Choose Your Text")
    st.markdown("Start by selecting a text type. This will be the basis for our analysis in the following steps.")
    
    choice = st.radio("Choose your input type:", options=["Social media post", "Review", "Article", "Your own text"])
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
    with stylable_container(key="blue_container", css_styles="{background-color: #238DFF; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""
                <p style='color: white;'>{text_input}</p>
                 """, unsafe_allow_html=True)
    
    if source:
        st.caption(f"[Source]({source})")
            
    col1, col2, col3 = st.columns(3)
    with col3:
        if st.button("Begin Analysis", on_click=lambda: st.session_state.update(step=st.session_state.step + 1, text_input=text_input), use_container_width=True):
            st.rerun()

# Step 2: Initial analysis
def step2():
    st.write("### Step 2: Initial Text Analysis")
    help="""Try different prompts, and see what results you get. Try to get a response in following format:\n\n
    {{
        "entities": ["entity1", "entity2", ...],
        "topics": ["topic1", "topic2", ...],
    }}"""
    st.markdown("Now that you've selected your text, let's perform an initial analysis. Instruct the LLM to identify key elements such as entities, main topics, writing style, or target audience.",
                help=help)
    with st.expander("**Selected Text**"):
        st.markdown(st.session_state.text_input, unsafe_allow_html=True)

    user_prompt = st.chat_input("Write your prompt here:")

    if user_prompt:
        st.session_state.llm_response_step_2 = get_llm_response(f"Text: {st.session_state.text_input}\nInstruction: {user_prompt}")
        st.session_state.question = user_prompt
    
    if st.session_state.llm_response_step_2:
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col1:
            st.write("🤖")
        with col2:
            with st.container():
                st.markdown(f"{st.session_state.llm_response_step_2}")

        col1, col2, col3 = st.columns(3, vertical_alignment='center')
        if col3.button("Continue to Step 3", on_click=lambda: st.session_state.update(step=st.session_state.step + 1), use_container_width=True):
            st.rerun()

# New function for sentiment analysis step
def step3():
    st.write("### Step 3: Sentiment Analysis")
    help="Try to modify your prompt to get only the numerical sentiment score as a result, without any additional information. For example, you could ask for 'just the number' or 'only the score'."
    st.markdown("Let's perform a sentiment analysis on the text to understand its overall emotional tone. Your goal is to generate an output that quantifies the sentiment on a scale from -1 (highly negative) to 1 (highly positive), as demonstrated in the presentation.",
                help=help)
    with st.expander("**Selected Text**"):
        st.markdown(st.session_state.text_input, unsafe_allow_html=True)

    user_prompt = st.chat_input("Write your prompt here:")
    
    if user_prompt:
        st.session_state.llm_response_step_3 = get_llm_response(f"Text: {st.session_state.text_input}\nInstruction: {user_prompt}")
        st.session_state.question = user_prompt
    
    if st.session_state.llm_response_step_3:
        # Display user question and AI response
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col1:
            st.write("🤖")
        with col2:
            with st.container():
                st.markdown(f"{st.session_state.llm_response_step_3}")

        col1, col2, col3 = st.columns(3, vertical_alignment='center')
        if col3.button("Continue to Step 4", on_click=lambda: st.session_state.update(step=st.session_state.step + 1), use_container_width=True):
            st.rerun()

# Step 4: Create structured data
def step4():
    st.write("### Step 4: Create Structured Data")
    help="If the JSON output isn't as expected, consider refining your prompt. You could explicitly specify the desired format, such as: 'Please respond using the following JSON structure:'"
    st.markdown("Now, instruct the AI to convert the extracted key elements and sentiment analysis into a structured JSON format.",
                help=help)
    with st.expander("**Selected Text**"):
        st.markdown(st.session_state.text_input, unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
    with col1:
        st.write("🤖")
    with col2:
        with st.container():
            st.write("**Extracted Key Elements from Initial Analysis:**")
            st.markdown(f"{st.session_state.llm_response_step_2}")
            st.write("**Sentiment Analysis Results:**")
            st.markdown(f"{st.session_state.llm_response_step_3}")
    
    user_prompt = st.chat_input("Write your prompt here:")
    
    if user_prompt:
        st.session_state.llm_response_step_4 = get_llm_response(f"Text: {st.session_state.llm_response_step_2}\nSentiment: {st.session_state.llm_response_step_3}\nInstruction: {user_prompt}")
        st.session_state.question = user_prompt
    
    if st.session_state.llm_response_step_4:
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col1:
            st.write("🤖")
        with col2:
            with st.container():
                try:
                    st.json(f"{st.session_state.llm_response_step_4}")
                except ValueError:
                    # If not valid JSON, display it as Markdown
                    st.markdown(st.session_state.llm_response_step_4)

        col1, col2, col3 = st.columns(3, vertical_alignment='center')
        if col3.button("Continue to Step 5", on_click=lambda: st.session_state.update(step=st.session_state.step + 1), use_container_width=True):
            st.rerun()
        
        
def create_network_graph(relationships):
    G = nx.Graph()
    for rel in relationships:
        G.add_edge(rel['entity1'], rel['entity2'], relationship=rel['relationship'])
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Entity Relationship Network")
    return plt

# Step 5: Generate visualizations
def step5():
    st.write("### Step 5: Visualize Relationships")
    help="""If you're not getting the expected output, try refining your prompt. Here's an example of a prompt that should work: 'Analyze the following text and provide a list of relationships between entities.\n\nRespond in the following JSON format:
    {
        "relationships": [
            {"entity1": "entity", "entity2": "entity", "relationship": "description"},
            ...
        ]
    }.'"""
    st.markdown("Let's identify relationships between entities in the text to create a visual network graph. The expected outcome here should include: 'entity1', 'entity2', and 'relationship' fields, ie:\n\n```json\n{\n  \"relationships\": [\n    {\"entity1\": \"Person A\", \"entity2\": \"Company B\", \"relationship\": \"works for\"},\n    {\"entity1\": \"Person C\", \"entity2\": \"Person A\", \"relationship\": \"collaborates with\"}\n  ]\n}\n```\n\nThis format will allow us to visualize the connections between entities effectively. Consider specifying this structure in your prompt.",
                help=help)
    
    with st.expander("**Selected Text**"):
        st.markdown(st.session_state.text_input, unsafe_allow_html=True)
    
    user_prompt = st.chat_input("Write your prompt here:")
    
    if user_prompt:
        st.session_state.llm_response_step_5 = get_llm_response(f"Text: {st.session_state.text_input}\nInstruction: {user_prompt}")
        st.session_state.question = user_prompt
    
    if st.session_state.llm_response_step_5:
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            with stylable_container(key="grey_container", css_styles="{background-color: #F7F7F7; border-radius: 0.5rem; padding: calc(1em - 1px); margin-top: 20px;}"):
                with st.container():
                    st.markdown(f"""{st.session_state.question}""")
        ""
        col1, col2 = st.columns([0.05, 0.95], vertical_alignment='top')
        with col1:
            st.write("🤖")
        with col2:
            with st.container():
                raw_content = st.session_state.llm_response_step_5

                # Attempt to parse the raw_content as JSON first
                try:
                    analysis = json.loads(raw_content)
                    # Display the parsed JSON
                    st.json(analysis)
                    
                    # Ensure the response contains the 'relationships' key
                    if 'relationships' in analysis:
                        # Generate and display the network graph
                        network_graph = create_network_graph(analysis['relationships'])
                        st.pyplot(network_graph)
                    else:
                        st.error("The response did not contain the expected 'relationships' field.")
                except json.JSONDecodeError:
                    # If JSON parsing fails, handle code blocks or other formats
                    if raw_content.startswith("```") and raw_content.endswith("```"):
                        raw_content = raw_content.strip("```").strip()
                    raw_content = raw_content.replace("json", "").strip()

                    # Try to parse the modified content as JSON again
                    try:
                        analysis = json.loads(raw_content)
                        # Display the parsed JSON
                        st.json(analysis)
                        
                        # Ensure the response contains the 'relationships' key
                        if 'relationships' in analysis:
                            # Generate and display the network graph
                            network_graph = create_network_graph(analysis['relationships'])
                            st.pyplot(network_graph)
                        else:
                            st.error("The response did not contain the expected 'relationships' field.")
                    except json.JSONDecodeError:
                        # If JSON parsing fails again, display the raw content as markdown
                        st.markdown(raw_content)
                        st.warning("Cannot create network graph. The response is not in JSON format.")

        col1, col2, col3 = st.columns(3, vertical_alignment='center')
        if col3.button("Continue to Step 6", on_click=lambda: st.session_state.update(step=st.session_state.step + 1), use_container_width=True):
            st.rerun()

# Step 6: Create an interactive summary
def step6():
    st.write("### Step 6: Final Report")
    st.success("Congratulations! You've completed all steps. 🥳 Here's the final output of your analysis!")
    st.write("Going from unstructured text input..")
    with stylable_container(key="blue_container", css_styles="{background-color: #238DFF; border-radius: 0.5rem; padding: 1em; margin-top: 10px;}"):
        with st.container():
            st.markdown(f"""
                <p style='color: white;'>{st.session_state.text_input}</p>
                 """, unsafe_allow_html=True)
    
    st.write("..to structured:")

    try:
        st.json(f"{st.session_state.llm_response_step_4}")
    except ValueError:
        # If not valid JSON, display it as Markdown
        st.markdown(st.session_state.llm_response_step_4)
    
    raw_content = st.session_state.llm_response_step_5

    # Attempt to parse the raw_content as JSON first
    try:
        analysis = json.loads(raw_content)
        # Display the parsed JSON
        st.json(analysis)
        
        # Ensure the response contains the 'relationships' key
        if 'relationships' in analysis:
            # Generate and display the network graph
            network_graph = create_network_graph(analysis['relationships'])
            st.pyplot(network_graph)
        else:
            st.error("The response did not contain the expected 'relationships' field.")
    except json.JSONDecodeError:
        # If JSON parsing fails, handle code blocks or other formats
        if raw_content.startswith("```") and raw_content.endswith("```"):
            raw_content = raw_content.strip("```").strip()
        raw_content = raw_content.replace("json", "").strip()

        # Try to parse the modified content as JSON again
        try:
            analysis = json.loads(raw_content)
            # Display the parsed JSON
            st.json(analysis)
            
            # Ensure the response contains the 'relationships' key
            if 'relationships' in analysis:
                # Generate and display the network graph
                network_graph = create_network_graph(analysis['relationships'])
                st.pyplot(network_graph)
            else:
                st.error("The response did not contain the expected 'relationships' field.")
        except json.JSONDecodeError:
            # If JSON parsing fails again, display the raw content as markdown
            st.markdown(raw_content)
            st.warning("Cannot create network graph. The response is not in JSON format.")

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

