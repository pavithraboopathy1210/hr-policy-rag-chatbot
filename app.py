
import streamlit as st
from QueryProcessor import process_user_query

st.set_page_config(
    page_title="HR Policy Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 HR Policy Chatbot")
st.caption("Ask questions about the HR policy document.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_query = st.chat_input("Ask your HR policy question...")

if user_query:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate chatbot response
    with st.chat_message("assistant"):

        with st.spinner("Searching HR policies..."):

            try:
                response = process_user_query(user_query)
                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
