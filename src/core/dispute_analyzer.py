import os
import openai
from src.prompt.identify_category import category_system_prompt

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
                {"role": "system", "content": category_system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.0
        )

        return (response.choices[0].message.content)
        
if __name__ == "__main__":
    import src.prompt
    print(dir(src.prompt))  # This will show all accessible attributes in src.prompt
