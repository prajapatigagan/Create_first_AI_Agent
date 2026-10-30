import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent


class ResearchResponse(BaseModel):
    topic: str = Field(description="Research topic")

    summary: str = Field(description="Research summary")

    sources: list[str] = Field(description="Sources used")

    tools_used: list[str] = Field(description="Tools used")

# llm model
llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)

agent = create_agent(

    model=llm,

    tools=[],

    system_prompt="""
    You are a research assistant.

    Answer the user's research query.

    Provide accurate and structured information.
    If no external sources or tools are used,
    return empty lists for sources and tools_used.
    """,

    response_format=ResearchResponse
)

raw_response = agent.invoke({

    "messages": [
        {
            "role": "user",
            "content": "What is the capital of India?"
        }
    ]

})

print(raw_response["structured_response"])

try:
    structured_response = raw_response["structured_response"]
    print(structured_response)
except KeyError:
    print("Error: Structured response not found.",raw_response)