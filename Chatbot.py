from dotenv import load_dotenv
import streamlit as st
from utils._admin_util import invoke_rag, get_ticket_category
import os

# Initialize categories in session state
if "categories" not in st.session_state:
    st.session_state.categories = {
        "HR Support": [],
        "IT Support": [],
        "Transportation Support": [],
        "Other": []
    }

def main():
    load_dotenv()
    
    # Page configuration
    st.set_page_config(
        page_title="Intelligent Customer Support Agent",
        page_icon="🤖",
        layout="wide"
    )

    # Sidebar for API key
    with st.sidebar:
        #openai_api_key = st.text_input("OpenAI API Key", type="password")
        st.markdown("---")
        st.markdown("""
        ### About
        This is an AI-powered customer support agent that can answer questions or raise support ticket about the company policies and procedures:
        - HR policies
        - IT policies
        - Transportation policies
        - Other policies
        """)
        
    # Set OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI API key not found! Please check your .env file.")
        st.stop()

    # Main chat interface
    st.title("🤖 Intelligent Customer Support Agent")
    st.caption("Your 24/7 AI Customer Service Representative")


    st.header("Automatic Ticket Classification Tool")
    #Capture user input
    st.write("We are here to help you, please ask your question:")
    prompt = st.text_input("🔍")

    if prompt:
        if "vector_store" not in st.session_state:
            st.error("Please load the document data first!")
            st.stop()
        
        response = invoke_rag(st.session_state.vector_store, prompt)
        st.write(response)

        #Button to create a ticket with respective department
        button = st.button("Submit ticket?")
        
        if button:
            category = get_ticket_category(prompt)
            st.session_state.categories[category].append(prompt)
            st.success("Ticket submitted successfully!")
            # Display category (optional)
            st.write(f"Category: {category}")
        

if __name__ == '__main__':
    main()

