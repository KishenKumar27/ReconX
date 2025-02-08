import openai
from dotenv import load_dotenv
import os

load_dotenv()

class StandardizeFormatCodeGenerator:
    def __init__(self, input_row):
        self.client = openai.OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=os.getenv["TOGETHER_API_KEY"],
        )
        self.model="deepseek-ai/DeepSeek-V3"

    def generate(self):
        return self.code.replace(' ', '').replace('\n', '')