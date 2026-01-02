# Salesforce SOQL Agent 🤖

An AI-powered Salesforce SOQL Assistant built using **LangGraph**, **LangChain**, and **Azure OpenAI**.

## 🚀 Features
- Natural language → SOQL planning
- Step-by-step query building
- Salesforce schema discovery
- Tool-driven execution
- Streamlit chat UI

## 🏗 Architecture
- LangGraph state machine
- Tool-first SOQL execution
- Secure Salesforce OAuth
- Azure OpenAI LLM

## 📦 Setup

```bash
1️⃣ Clone Repo
git clone https://github.com/yashvardhan599/salesforce-soql-agent.git

2️⃣ Create Virtual Env
python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment
cp .env.example .env

Fill in Azure OpenAI & Salesforce credentials.

5️⃣ Run App
streamlit run streamlit_app.py