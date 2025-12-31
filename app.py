import streamlit as st
from agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

def clean_message_content(content):
    """Extracts plain text from complex model responses."""
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                return item.get('text')
        return str(content)
    return content

st.set_page_config(page_title="Multi-Agent AI Analyst", page_icon="📈")

st.title("📈 Multi-Agent Financial Analyst")
st.markdown("""
This system operates on a **Multi-Agent Architecture**:
1. **Supervisor**: Coordinates the workflow.
2. **Market Analyst**: Specialist in stock prices and market data.
3. **News Researcher**: Specialist in global news and trend analysis.
""")

if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        if not msg.tool_calls:
            with st.chat_message("assistant"):
                st.markdown(clean_message_content(msg.content))

if prompt := st.chat_input("Ask about a stock or compare companies..."):
    
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Supervisor is coordinating the team..."):
            try:
                langfuse_handler = CallbackHandler()

                config = {
                    "configurable": {"thread_id": st.session_state.thread_id},
                    "callbacks": [langfuse_handler],
                    "run_name": "Multi_Agent_Financial_Analysis"
                }

                input_data = {"messages": st.session_state.messages}
                response = st.session_state.agent.invoke(input_data, config)
                
                st.session_state.messages = response["messages"]
                
                final_response = response["messages"][-1].content
                final_text = clean_message_content(final_response)
                
                st.markdown(final_text)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

st.sidebar.title("Settings")
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()

st.sidebar.divider()
st.sidebar.info(f"**Session Thread ID:** \n`{st.session_state.thread_id}`")