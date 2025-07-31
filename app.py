# Import the Streamlit library for creating web apps
import os
import streamlit as st
from functions import *

# Define the main function
def main():
    # Set the title of the web app
    st.title("PDF Insight Assistant")
    # Create a file uploader widget to upload PDF files
    uploaded_file = st.file_uploader("Choose a PDF file to upload", type="pdf")
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Create a button labeled "Read PDF" and check if it's clicked
        if st.button("Read PDF"):
            # Save the uploaded file
            save_uploaded_file(uploaded_file)
            # Display a message
            st.write("Please wait while we learn the PDF.")
            # Update the assistant's knowledge base with the PDF content
            update_assistant_knowledgebase(uploaded_file.name)
            # Display a message
            st.write("PDF reading completed! Now you may ask a question")
            # Remove the saved PDF file from the server
            # os.remove(uploaded_file.name)
    # Create a text input box for the user to enter their query
    user_input = st.text_input("Enter your Query:")
    # Create a button labeled "Send" and check if it's clicked
    if st.button("Send"):
        # Display the user's query
        st.write("You:", user_input)
        # Get the response from the assistant
        response = get_assistant_response(user_input)
        # Display the assistant's response
        st.write("GPT: "+response)
# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    # Call the main function
    main()