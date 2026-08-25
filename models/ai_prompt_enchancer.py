from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

class AIEnchancer():
    def __init__(self, model, sys_prompt):
        self.llm = ChatOpenAI(model=model)
        self.sys_prompt = sys_prompt

    def run(self, question):
        messages = [
            SystemMessage(content=self.sys_prompt),
            HumanMessage(content=question)
        ]
        response = self.llm.invoke(messages)
        tokens = self.get_token_usage(response=response)
        return {
            "content": response.content,
            "tokens": tokens
        }

    def get_token_usage(self, response):
        usage = response.response_metadata.get("token_usage", {})
        return {
            "prompt_tokens": usage.get('prompt_tokens', 0),
            "completion_tokens": usage.get('completion_tokens', 0),
            "total_tokens": usage.get('total_tokens', 0)
        }
