import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv(override=True)

llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    model=os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    temperature=0.1
)
