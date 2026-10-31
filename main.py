# import traceback
# from dotenv import load_dotenv

# load_dotenv()

# from pydantic import BaseModel, Field
# from langchain_groq import ChatGroq
# from langchain_core.messages import ToolMessage
# from langchain.agents import create_agent
# from tools import search_tool, wiki_tool, save_to_txt


# class ResearchResponse(BaseModel):
#     topic: str = Field(description="Research topic")
#     summary: str = Field(description="Concise, structured research summary")
#     sources: list[str] = Field(
#         default_factory=list, description="URLs or names of sources used"
#     )
#     tools_used: list[str] = Field(
#         default_factory=list, description="Tools used (filled automatically)"
#     )


# llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0,max_tokens=4000)

# agent = create_agent(
#     model=llm,
#     tools=[search_tool, wiki_tool],
#     system_prompt=(
#         "You are a research assistant. Use the tools for factual or current "
#         "information. Give an accurate, structured answer and mention the "
#         "source names or URLs you used."
#     ),
# )

# structurer = llm.with_structured_output(ResearchResponse, method="json_schema")


# def get_tools_used(messages) -> list[str]:
#     """Actual tool calls se tool names nikalo (LLM pe depend nahi)."""
#     return sorted({m.name for m in messages if isinstance(m, ToolMessage)})


# def to_structured(query: str, answer: str) -> ResearchResponse:
#     """Answer ko ResearchResponse mein convert karo, fail ho to fallback."""
#     try:
#         return structurer.invoke(
#     f"Query: {query}\n\nResearch answer:\n{answer}\n\n"
#     "Convert this into the schema. IMPORTANT: Do NOT shorten or summarise. "
#     "Keep the full detailed text in 'summary', and extract 8-12 key_points "
#     "and the sources."
# )
#     except Exception:
#         traceback.print_exc()
#         print("\n[Structured output fail hua, plain answer se fallback]\n")
#         return ResearchResponse(topic=query, summary=answer)


# def main():
#     query = input("What can I help you research? ").strip()
#     if not query:
#         print("Query empty hai.")
#         return

#     try:
#         raw = agent.invoke({"messages": [{"role": "user", "content": query}]})
#     except Exception:
#         traceback.print_exc()
#         return

#     answer = raw["messages"][-1].content
#     result = to_structured(query, answer)
#     result.tools_used = get_tools_used(raw["messages"])

#     output = result.model_dump_json(indent=2)
#     print(output)
#     print(save_to_txt(output))


# if __name__ == "__main__":
#     main()






