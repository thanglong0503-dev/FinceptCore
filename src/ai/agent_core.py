# src/ai/agent_core.py
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from src.ai.tools import FinancialTools
import os

class FinceptAgent:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(
            temperature=0, 
            model="gpt-4-turbo", 
            openai_api_key=api_key
        )
        self.tools =
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        self.agent_chain = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )

    def run(self, query):
        """Thực thi câu hỏi của người dùng"""
        try:
            return self.agent_chain.run(query)
        except Exception as e:
            return f"Xin lỗi, tôi gặp sự cố khi xử lý yêu cầu: {str(e)}"
