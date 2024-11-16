import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the system prompt
system_prompt = """
You are a highly experienced ESG consulting expert with years of experience in BCG, Bain, and McKinsey. You support users on:
- ESG Risk and Opportunity Assessment
- ESG Strategy Recommendations
- ESG Performance Analytics
- ESG Report Summarization
- Benchmarking Reports
- Compliance Checks
- Forecasting and Simulations

Provide clear, professional, and detailed responses to the user's queries. If you are unsure or need more information, ask clarifying questions to help the user articulate their needs better.
"""

# Initialize the session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.title("🌿 ESG Consulting Expert Chatbot")

st.write("Welcome! I'm here to assist you with all your ESG consulting needs. How can I help you today?")

# User input
user_input = st.text_input("Your question:", key="user_input")

if user_input:
    # Append user's message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Generate assistant's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            max_tokens=500,
            temperature=0.7,
        )

        assistant_reply = response.choices[0].message["content"]

        # Append assistant's message to the conversation
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # Display the conversation
        for message in st.session_state.messages[1:]:  # Skip the system prompt
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"**ESG Expert:** {message['content']}")

    except AttributeError as e:
        st.error("An error occurred with the OpenAI API call.")
        st.error(str(e))

    # Clear the input box after submission
    st.session_state.user_input = ""
