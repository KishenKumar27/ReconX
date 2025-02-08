import ast
import favicon
import os
import traceback
import tiktoken  # Import tiktoken for token counting

from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
from ..prompt.forex import system_prompt as forex_analyzer_system_prompt, user_prompt as forex_analyzer_user_prompt
from ..tool.macroeconomic import search_economic_data
from ..tool.news import search_news_articles

load_dotenv()

class ForexSentimentAnalyzer():
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Load tokenizer
        
        llm = ChatCohere(
            model=os.getenv("COHERE_MODEL"),
            temperature=float(os.getenv("CHATBOT_TEMPERATURE")),
            cohere_api_key=os.getenv("COHERE_API_KEY"),
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", forex_analyzer_system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", forex_analyzer_user_prompt),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        tools = [
            search_news_articles,
            search_economic_data,
        ]
        
        agent = create_tool_calling_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            early_stopping_method="generate",
        )

    def count_tokens(self, text):
        """Helper function to count tokens in a given text."""
        return len(self.tokenizer.encode(text))

    def get_sentiment(self, name: str):
        """
        Retrieves forex sentiment analysis based on macroeconomic factors, geopolitical events, and market sentiment.
        """
        input_text = f"Forex Pair: {name}"
        
        # Count tokens before processing
        input_tokens = self.count_tokens(input_text)
        system_tokens = self.count_tokens(forex_analyzer_system_prompt)
        user_tokens = self.count_tokens(forex_analyzer_user_prompt)
        total_input_tokens = input_tokens + system_tokens + user_tokens
        
        print(f"[Token Usage] Input: {input_tokens}, System: {system_tokens}, User: {user_tokens}, Total Before LLM: {total_input_tokens}")

        # Invoke the LLM agent
        forex_analysis = self.agent_executor.invoke(
            {"forex_pair": name},
            return_only_output=True,
        )

        # Count tokens from model response
        output_text = forex_analysis.get("output", "")
        output_tokens = self.count_tokens(output_text)
        
        print(f"[Token Usage] Output: {output_tokens}, Total Tokens Used: {total_input_tokens + output_tokens}")

        if "output" in forex_analysis:
            json_string = output_text.replace('```json\n', '').replace('\n```', '')

            try:
                forex_analysis = ast.literal_eval(json_string)
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                forex_analysis = {"error": "Invalid response format"}

        # Adding favicons for each news_source
        if 'news_sources' in forex_analysis:
            for news_source in forex_analysis['news_sources']:
                try:
                    icons = favicon.get(news_source.get("url", ""))
                    news_source['image'] = icons[0].url if icons else ""  # Handle empty result
                except Exception as e:
                    news_source['image'] = ""  # Default to None if fetching fails
                    print(f"Error fetching favicon for {news_source.get('url', '')}: {e}")

        return forex_analysis