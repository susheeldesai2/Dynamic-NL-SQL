from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import sqlite3
import pandas as pd
import os

# Load environment variables
load_dotenv()

def get_table_schema(table_name, db_name="user_uploaded.db"):
    """Fetches the schema of the given table from the SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    if not columns:
        raise ValueError(f"Table {table_name} does not exist or has no columns.")
    
    schema = {col[1]: col[2] for col in columns}  # col[1] is column name, col[2] is datatype
    conn.close()
    
    return schema

def generate_sql_prompt(table_name, schema):
    """Creates a dynamic SQL generation prompt based on the table schema."""
    column_details = "\n".join([f"{col}: {dtype}" for col, dtype in schema.items()])
    
    template = f"""You are an intelligent assistant that converts natural language queries into SQL queries. 
Your task is to take a natural language question and return only the SQL query.

IMPORTANT:
- Only return the SQL query.
- Do not include any explanations, just return the query.
- Ensure the SQL query is clean and without additional text.

The table you are working with is named `{table_name}`. Here are its columns:

{column_details}

Now, based on the information provided, convert the following natural language question into an SQL query.

Ensure that you return only the SQL query, with no additional explanations.

Question: {{question}}
"""
    return template

def execute_sql_query(query, db_name="user_uploaded.db"):
    """Executes the generated SQL query and returns the results."""
    conn = sqlite3.connect(db_name)
    try:
        result_df = pd.read_sql_query(query, conn)
        conn.close()
        return result_df
    except Exception as e:
        conn.close()
        return f"SQL Execution Error: {e}"

if __name__ == "__main__":
    # Get the dynamically created table name
    table_name = input("Enter the name of the uploaded table: ").strip()

    # Fetch the schema dynamically
    schema = get_table_schema(table_name)

    # Generate dynamic SQL generation prompt
    prompt_template = generate_sql_prompt(table_name, schema)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["question"]
    )

    # Create LLM object
    llm = ChatGroq(temperature=0, model="llama3-70b-8192")

    # Accept user query
    user_query = input("Ask a question about your data: ").strip()

    # Generate SQL Query
    chain = prompt | llm
    response = chain.invoke({"question": user_query})
    sql_query = response.content.strip()
    
    print("\nGenerated SQL Query:")
    print(sql_query)

    # Execute SQL Query
    query_result = execute_sql_query(sql_query)
    
    print("\nQuery Results:")
    print(query_result)
