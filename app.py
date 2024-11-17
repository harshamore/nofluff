import streamlit as st
from openai import OpenAI
import os

# Page configuration
st.set_page_config(
    page_title="ESG Consulting Expert",
    page_icon="🌍",
    layout="wide"
)

# Check for OpenAI API key in Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Please set the OPENAI_API_KEY in your Streamlit secrets!")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main content
st.title("🌍 ESG Consulting Expert")
st.markdown("Your virtual ESG consultant with experience from top consulting firms")

# Sidebar content
with st.sidebar:
    st.markdown("### Areas of Expertise")
    st.markdown("""
    - ESG Risk & Opportunity Assessment
    - Strategy Recommendations
    - Performance Analytics
    - Report Summarization
    - Benchmarking Reports
    - Compliance Checks
    - Forecasting & Simulations
    """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This AI consultant combines expertise from:
    - BCG
    - Bain
    - McKinsey
    
    For comprehensive ESG consulting support.
    """)

# System message defining the AI's role and capabilities
system_message = """You are an expert ESG consultant with extensive experience from top consulting firms including BCG, Bain, and McKinsey. 

Your expertise covers:
1. ESG Risk and Opportunity Assessment
2. ESG Strategy Recommendations
3. ESG Performance Analytics
4. ESG Report Summarization
5. Benchmarking Reports
6. Compliance Checks
7. Forecasting and Simulations

Guidelines for your responses:
- Provide specific, actionable insights based on industry best practices
- If a query is unclear or lacks context, ask clarifying questions
- Support recommendations with relevant frameworks and methodologies
- Consider industry-specific nuances and regulatory requirements
- When appropriate, suggest metrics and KPIs for tracking progress
- If uncertain about specific details, ask for more information rather than making assumptions
- Use structured approaches (e.g., matrices, frameworks) when applicable
- Provide specific examples and case studies when relevant
- Include quantitative metrics and benchmarks when possible
- Suggest implementation timelines and resource requirements when appropriate

Always maintain a professional yet approachable consulting tone.

If the user's query is unclear or lacks essential context, ask specific questions to better understand:
1. Industry/sector
2. Company size
3. Geographic region
4. Current ESG maturity level
5. Specific challenges or goals
6. Timeline and resource constraints"""

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What ESG-related questions can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare messages including system message
            messages = [
                {"role": "system", "content": system_message}
            ] + st.session_state.messages
            
            # Get streaming response from OpenAI
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": m["role"], "content": m["content"]} for m in messages],
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit and OpenAI GPT-4*")
