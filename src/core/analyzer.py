import ast
import favicon
import os
import traceback

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

    def get_sentiment(
        self,
        name: str,
    ):
        # macroeconomic factors, geopolitical events, and market sentiment
        forex_analysis = self.agent_executor.invoke(
            {
                "forex_pair": name,
            },
            return_only_output=True,
        )

        if "output" in forex_analysis:
            # Extracting the JSON string from the 'output' key and removing the '```json' and '```' parts
            json_string = forex_analysis['output'].replace('```json\n', '').replace('\n```', '')

            # Converting the string into a Python dictionary
            forex_analysis = ast.literal_eval(json_string)

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