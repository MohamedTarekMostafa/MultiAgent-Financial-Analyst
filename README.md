# 📈 Multi-Agent Financial Analyst

An advanced AI-powered financial research system built with **LangGraph** and **Gemini 2.5- Flash**. This project uses a **Supervisor-Worker architecture** to coordinate specialized agents for market data analysis and global news research.

## 🧠 System Architecture

The project implements a **Multi-Agent Orchestration** pattern:

* **Supervisor (The Manager)**: Acts as the brain of the system. It receives user queries, plans the workflow, and delegates tasks to specialized agents.
* **Market Analyst**: A worker agent specialized in quantitative data. It uses `yfinance` to fetch real-time stock prices and daily changes.
* **News Researcher**: A worker agent specialized in qualitative research. It uses the `Tavily Search API` to find and summarize market-moving news and trends.
* **State Management**: Uses a shared state with `MemorySaver` to allow the agents to remember user preferences and past context within a `thread_id`.



## 🚀 Features

* **Autonomous Delegation**: The Supervisor decides whether to check prices, search news, or both based on the user's intent.
* **Contextual Memory**: Remembers specific user goals (e.g., "I have a $50k investment target") across the entire conversation.
* **Real-time Observability**: Fully integrated with **Langfuse** for tracing, cost tracking, and monitoring agent hand-offs.
* **Modern UI**: An interactive Chat interface built with **Streamlit**.

## 🛠️ Tech Stack

* **Orchestration**: LangChain & LangGraph
* **LLM**: Google Gemini 2.5 Flash
* **Search**: Tavily AI
* **Data**: Yahoo Finance (yfinance)
* **Monitoring**: Langfuse
* **Frontend**: Streamlit

## 📸 Screenshots

### 1. User Interface (Streamlit)
*![WhatsApp Image 2025-12-31 at 11 17 46 PM](https://github.com/user-attachments/assets/8f018f9f-8752-408f-a832-47e0465b5c53)*

### 2. Agent Workflow (LangGraph)
*![WhatsApp Image 2025-12-31 at 10 51 10 PM](https://github.com/user-attachments/assets/0602004a-ce88-465c-a770-064a021c64a1)





