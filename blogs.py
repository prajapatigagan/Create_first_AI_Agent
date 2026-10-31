import traceback
from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_to_txt

class SocialContent(BaseModel):
    topic: str = Field(description="Topic of the content")
    linkedin_post: str = Field(
        description="Professional LinkedIn post (150-250 words): strong hook, "
        "short paragraphs, key insights, closing question/CTA"
    )
    twitter_thread: list[str] = Field(
        description="Twitter/X thread of 5-8 tweets, each STRICTLY under 280 "
        "characters. First tweet = hook, last tweet = CTA. Number them like 1/7"
    )
    instagram_caption: str = Field(
        description="Casual Instagram caption with hook, emojis, line breaks "
        "and a CTA"
    )
    hashtags: list[str] = Field(
        default_factory=list, description="8-12 relevant hashtags (with #)"
    )
    sources: list[str] = Field(
        default_factory=list, description="URLs or names of sources used"
    )
    tools_used: list[str] = Field(
        default_factory=list, description="Tools used (filled automatically)"
    )


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=2000,
    reasoning_effort="low",   # sabse bada speedup
)

writer_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    max_tokens=3000,
    reasoning_effort="low",
)

agent = create_agent(
    model=llm,
    tools=[search_tool, wiki_tool],
    system_prompt=(
        "You are a research assistant. Make AT MOST 2 tool calls total, "
        "call them together in parallel if possible. Then give short research "
        "notes (key facts, stats, source names/URLs) in under 300 words."
    ),
)
writer = writer_llm.with_structured_output(SocialContent, method="json_schema")

def get_tools_used(messages) -> list[str]:
    """Actual tool calls se tool names nikalo (LLM pe depend nahi)."""
    return sorted({m.name for m in messages if isinstance(m, ToolMessage)})

def write_content(query: str, research: str) -> SocialContent:
    """Research notes se social media content likho, fail ho to fallback."""
    try:
        return writer.invoke(
            f"Topic: {query}\n\nResearch notes:\n{research}\n\n"
            "Using ONLY the facts in the research notes, write content for "
            "LinkedIn, Twitter/X and Instagram. Make each platform's tone "
            "different (LinkedIn = professional, Twitter = punchy, "
            "Instagram = casual). Do not invent facts or stats. "
            "Also list the sources used."
        )
    except Exception:
        traceback.print_exc()
        print("\n[Structured output fail hua, plain research se fallback]\n")
        return SocialContent(
            topic=query,
            linkedin_post=research,
            twitter_thread=[],
            instagram_caption="",
        )

def main():
    query = input("Kis topic pe content chahiye? ").strip()
    if not query:
        print("Query empty hai.")
        return

    try:
        raw = agent.invoke({"messages": [{"role": "user", "content": query}]})
    except Exception:
        traceback.print_exc()
        return

    research = raw["messages"][-1].content
    result = write_content(query, research)
    result.tools_used = get_tools_used(raw["messages"])

    # Twitter limit check
    for i, tweet in enumerate(result.twitter_thread, 1):
        if len(tweet) > 280:
            print(f"[Warning] Tweet {i} {len(tweet)} chars ka hai (limit 280)")

    output = result.model_dump_json(indent=2)
    print(output)
    print(save_to_txt(output))


if __name__ == "__main__":
    main()    