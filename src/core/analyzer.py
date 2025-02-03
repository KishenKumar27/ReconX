import ast
import os

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

            # # Formatting the 'news_sources' field as a string with links
            # if 'news_sources' in forex_analysis:
            #     news_sources = forex_analysis['news_sources']
                
            #     # Create a formatted string with URLs and titles
            #     formatted_news_sources = ', '.join(
            #         [f"{i+1}. [{news['title']}]({news['url']})" for i, news in enumerate(news_sources)]
            #     )
                
            #     # Update the 'news_sources' field with the formatted string
            #     forex_analysis['news_sources'] = formatted_news_sources

        return forex_analysis