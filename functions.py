# Import necessary libraries
import json
from openai import OpenAI
import time

# Load the API key from the JSON file
with open(r"C:\Users\RITESH PATIL\Downloads\PDF Document Analyzer - GenAI - Ivy Pro School\PDF Document Analyzer - GenAI\open_ai_api.json") as f:
    api_key_data = json.load(f)

# Initialize the OpenAI client with the extracted API key
client = OpenAI(api_key=api_key_data['api_key'])

# set the assistant ID
assistant_id = api_key_data['assistant_id']

# Create a new thread for conversation
thread = client.beta.threads.create()
# Store the thread ID for future use
thread_id = thread.id

# Function to save the uploaded file locally
def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Function to get a response from the assistant
def get_assistant_response(query):

    threadId = thread_id
    assistantId = assistant_id

    # Send the user query as a message in the thread
    message = client.beta.threads.messages.create(
    thread_id=threadId,
    role="user",
    content=query
        )
    
    # Create a run to get a response from the assistant
    run = client.beta.threads.runs.create(
    thread_id=threadId,
    assistant_id=assistantId,
    instructions="Use the user uploaded file to provide answer. Do not answer if you couldn't find any context in the knowledgebase. Just say I don't know"
    )
    
    while True:

        # Check Run Status
        run = client.beta.threads.runs.retrieve(thread_id=threadId,run_id=run.id)
        time.sleep(1)
        
        # Perform Actions based on run status
        # If Run status is 'completed' it means return the recent output
        if run.status == 'completed':
            messages_ = client.beta.threads.messages.list(thread_id=threadId)
            response = messages_.data[0].content[0].text.value
            return response

# Function to update the assistant's knowledge base with a new file 
def update_assistant_knowledgebase(filepath):
    # Retrieve the current assistant which already uploaded
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    
    # Upload the file to OpenAI and get its ID
    file = client.files.create(
        file=open(filepath, "rb"),
        purpose='assistants'
        )

    # Update the assistant with the valid file IDs
    my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    tools=[{"type": "retrieval"}],
    file_ids=[file.id],
    )
    print("Assistant updated with valid file IDs.")
    