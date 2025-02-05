import os
import openai


class DisputeAnalyzer():
    def __init__(self):
        self.client = openai.OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=os.environ["TOGETHER_API_KEY"],
        )
        self.model="deepseek-ai/DeepSeek-V3"

        
    def identify_category(self, message: str):
        response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": "You are a travel agent. Be descriptive and helpful."},
            {"role": "user", "content": "Tell me the top 3 things to do in San Francisco"},
        ]
        )

        print(response.choices[0].message.content)

    
        
