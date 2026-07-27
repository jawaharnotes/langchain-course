from typing import List
from pydantic import BaseModel, Field       #Basemodel --> Gives ability for data parsing, manipulation #Field --> Add Meta data, descriprtion to our artibutes
from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from tavily import TavilyClient
from langchain_tavily import TavilySearch


# tavily = TavilyClient()
# @tool
# def search(query: str) -> str:
#     """"Tool that searches over internet
#     Args:
#         query: The query to search for
#     Returns:
#         The Search Result
#         """
#     print(f"searching for {query}")
#     #return "Berlin weather is rainy"
#     return tavily.search(query=query)


class JobPosting(BaseModel):
    """One job posting returned by the agent."""

    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: str = Field(description="Job location")
    linkedin_url: str = Field(description="LinkedIn Job URL")
    summary: str = Field(
        description="Short summary of the job posting (2-3 sentences)"
    )

class AgentResponse(BaseModel):
    """Structured response returned by the agent."""
    jobs: List[JobPosting]



llm = ChatOllama(model="gpt-oss:20b",  temperature=0)
#tools = [search]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():

    prompt = """
You are an AI job search assistant.

Use the Tavily Search tool.

Search for exactly 3 LinkedIn job postings for:

AI Engineer
LangChain
Berlin, Germany

Search query:

site:linkedin.com/jobs AI Engineer LangChain Berlin Germany

For each job return:

- Job Title
- Company
- Location
- LinkedIn Job URL
- Short summary

Rules:

1. ONLY use information returned by the search tool.
2. DO NOT invent companies.
3. DO NOT generate resumes.
4. DO NOT rewrite job descriptions into candidate profiles.
5. Return ONLY 3 jobs.
"""

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=prompt)
            ]
        }
    )

    print("\n==============================")
    print("Agent Response")
    print("==============================\n")

    print(result)


if __name__ == "__main__":
    main()
