GenAI-powered Chatbot for Dynamic File Upload, Schema Fetching, and SQL Querying

This GenAI-powered chatbot enables dynamic interaction with datasets, where the source file is not static. The process begins with running the upload_data.py script, which allows users to upload a file. This file is then loaded into Python and stored within an SQLite database, providing a structured format for querying.

Once the file is uploaded, the main.py script is used to fetch the schema of the newly uploaded data dynamically. This allows the chatbot to automatically recognize the structure of the dataset, ensuring that subsequent SQL queries are accurate and contextually relevant.

Users can then interact with the chatbot by asking questions in natural language. The chatbot translates these queries into valid SQL statements based on the dynamic schema and executes them on the SQLite database. The results of these queries are returned in a clear and understandable format.

Key Features:

Dynamic File Upload: Users can upload a new file anytime via the upload_data.py script. The chatbot automatically loads this data into Python and stores it in SQLite for easy querying.

Dynamic Schema Fetching: The main.py script fetches the schema of the uploaded file dynamically, ensuring that the chatbot adapts to different datasets without requiring manual intervention.

Natural Language Querying: Users can ask questions in natural language, which the chatbot translates into SQL queries. This makes it simple for users to interact with the data without needing any prior knowledge of SQL.

SQL Query Execution and Results: The chatbot executes the generated SQL queries on the SQLite database and presents the results in a user-friendly format.

This project allows for flexible and dynamic interaction with datasets, empowering users to easily upload, query, and analyze data through a conversational interface.
