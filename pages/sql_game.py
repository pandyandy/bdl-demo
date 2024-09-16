import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect
import openai
import os
import time 
from openai import OpenAI 
# Set OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize session state
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

st.title(":joystick: SQL Prompt Game")
with st.sidebar:
    st.page_link('hello.py', label='Home', icon='🏡')
    st.title("Game Progress")
    st.text(f"Score: {st.session_state.score}")

# Sample data for levels
products_df = pd.DataFrame({
    'product_id': [1, 2, 3],
    'product_name': ['Widget', 'Gadget', 'Thingamajig'],
    'price': [19.99, 23.50, 11.00]
})

orders_df = pd.DataFrame({
    'order_id': [101, 102, 103],
    'product_id': [1, 2, 2],
    'quantity': [2, 1, 4]
})

client = OpenAI(api_key=st.secrets['api_key'])

# Create an in-memory SQLite database
engine = create_engine('sqlite://', echo=False)
products_df.to_sql('products', con=engine, index=False, if_exists='replace')
orders_df.to_sql('orders', con=engine, index=False, if_exists='replace')

def get_tables_schema(engine):
    inspector = inspect(engine)
    schemas = ""
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_definitions = [f"{col['name']} {str(col['type'])}" for col in columns]
        schemas += f"Table {table_name}: columns ({', '.join(column_definitions)})\n"
    return schemas

def generate_sql_from_prompt(prompt, tables_schema):
    system_prompt = f"You are an expert SQL assistant. Given the database schema:\n{tables_schema}\nGenerate an SQL query that fulfills the user's request. Return only the SQL query, no other text or comments."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0  # For deterministic output
    )
    sql_query = response.choices[0].message.content
    return sql_query.strip()

def execute_query(sql_query):
    try:
        result = pd.read_sql_query(sql_query, con=engine)
        return result
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return None

def calculate_score(is_correct, time_taken=0):
    total_score = 0
    if is_correct:
        total_score += 100
        # Calculate time penalty (max 30 points)
        time_penalty = min(100, int(time_taken / 2))  # Lose 1 point every 2 seconds, up to 30 points
        total_score -= time_penalty
    return total_score

def get_level_data(level):
    if level == 1:
        expected_result = products_df
        return products_df, "Retrieve all products from the database.", expected_result
    elif level == 2:
        expected_result = orders_df.groupby('product_id').agg({'quantity': 'sum'}).reset_index()
        expected_result = expected_result.rename(columns={'quantity': 'total_quantity'})
        return orders_df, "Find the total quantity ordered for each product. Return only product_id and count.", expected_result
    elif level == 3:
        expected_result = pd.merge(products_df, orders_df, on='product_id', how='left').groupby('product_name')['quantity'].sum().reset_index()
        expected_result = expected_result.rename(columns={'quantity': 'total_quantity_ordered'})
        expected_result['total_quantity_ordered'] = expected_result['total_quantity_ordered'].astype(int)
        return [products_df, orders_df], "Find the total quantity ordered for each product and display the product name. Return only product name and quantity.", expected_result
    elif level == 4:
        expected_result = pd.merge(products_df, orders_df, on='product_id')
        expected_result['total_price'] = expected_result['price'] * expected_result['quantity']
        expected_result = expected_result.groupby('order_id')['total_price'].sum().reset_index()
        expected_result = expected_result.rename(columns={'total_price': 'highest_total_value'})
        expected_result = expected_result.sort_values('highest_total_value', ascending=False).head(1)
        return [products_df, orders_df], "Find the order with the highest total value. Return the order_id and the total value.", expected_result
    elif level == 5:
        expected_result = pd.merge(products_df, orders_df, on='product_id', how='left')
        expected_result = expected_result[expected_result['order_id'].isnull()]
        expected_result = expected_result[['product_id', 'product_name', 'price']]
        expected_result = expected_result.sort_values('price', ascending=False)
        return [products_df, orders_df], "Identify products that haven't been ordered yet. Return the product ID, name, and price of these products, sorted by price from highest to lowest.", expected_result
    else:
        st.success("Congratulations! You've completed all levels.")
        st.stop()

table_df, task_description, expected_result = get_level_data(st.session_state.level)
st.write(f"## Level {st.session_state.level}")
st.write("**Task:** " + task_description)
st.write("**Table(s) you are working with:**")

if isinstance(table_df, list):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Table 1:")
        st.dataframe(table_df[0], use_container_width=True, hide_index=True)
    with col2:
        st.write("Table 2:")
        st.dataframe(table_df[1], use_container_width=True, hide_index=True)
else:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(table_df, use_container_width=True, hide_index=True)

st.write('**Expected Result:**')
col1, col2 = st.columns(2)
with col1:
    st.dataframe(expected_result, use_container_width=True, hide_index=True)

prompt = st.text_area("Write a prompt to generate the SQL query:")

if st.button("Submit"):
    if prompt:
        # Calculate time taken
        time_taken = time.time() - st.session_state.start_time
        
        # Get database schema
        tables_schema = get_tables_schema(engine)
        # Generate SQL using GPT-4
        with st.spinner('Generating SQL query...'):
            sql_query = generate_sql_from_prompt(prompt, tables_schema)
        
        # Check if the generated query is a valid SQL query
        if not sql_query.strip().lower().startswith(('select', 'with')):
            st.error("The generated query doesn't appear to be a valid SQL query. Please try again.")
            if st.button("Skip to Next Level", on_click=lambda: st.session_state.update(level=st.session_state.level + 1, score=st.session_state.score)):
                st.rerun()
        else:
            st.write("**Generated SQL Query:**")
            st.code(sql_query, language='sql')
            # Execute the SQL query
            result = execute_query(sql_query)
            if result is not None:
                st.write("**Query Result:**")
                st.dataframe(result, use_container_width=True, hide_index=True)
                
                # Validate result
                is_correct = result.reset_index(drop=True).equals(expected_result.reset_index(drop=True))
                
                # Debug information
                st.write("Debug Information:")
                st.write(f"Result shape: {result.shape}, Expected shape: {expected_result.shape}")
                st.write(f"Result dtypes: {result.dtypes}")
                st.write(f"Expected dtypes: {expected_result.dtypes}")
                
                if is_correct:
                    st.success(":tada: Correct!")
                    score = calculate_score(is_correct=True, time_taken=time_taken)
                    st.session_state.score += score
                    st.write(f"Time taken: {time_taken:.2f} seconds")
                    st.write(f"Score for this level: {score}")
                    st.session_state.level += 1
                    if st.button("Next Level", on_click=lambda: st.session_state.update(start_time=time.time())):
                        #st.session_state.start_time = time.time()  # Reset start time for next level
                        st.rerun()
                else:
                    st.error("The result is incorrect. Try again!")
                    if st.button("Skip to Next Level", on_click=lambda: st.session_state.update(level=st.session_state.level + 1)):
                        #st.session_state.level += 1
                        st.rerun()
            else:
                st.error("Failed to execute the SQL query. Please try again.")
                if st.button("Skip to Next Level", on_click=lambda: st.session_state.update(level=st.session_state.level + 1, score=st.session_state.score)):
                    st.rerun()
    else:
        st.warning("Please enter a prompt before submitting.")