

import streamlit as st

from blogs import agent, write_content, get_tools_used
from tools import save_to_txt

st.set_page_config(page_title="Social Content Generator", page_icon="✍️", layout="wide")
st.title("✍️ Social Media Content Generator")
st.caption("Topic do, research + LinkedIn / Twitter / Instagram content ready.")

topic = st.text_input("Kis topic pe content chahiye?", placeholder="e.g. Rise of AI agents in 2026")
generate = st.button("Generate", type="primary")

if generate:
    if not topic.strip():
        st.warning("Topic daalo pehle.")
    else:
        try:
            with st.spinner("Research ho raha hai..."):
                raw = agent.invoke({"messages": [{"role": "user", "content": topic.strip()}]})
            research = raw["messages"][-1].content

            with st.spinner("Content likha ja raha hai..."):
                result = write_content(topic.strip(), research)
            result.tools_used = get_tools_used(raw["messages"])

            st.session_state["result"] = result
        except Exception as e:
            st.error(f"Error aaya: {e}")

result = st.session_state.get("result")

if result:
    tab_li, tab_tw, tab_ig = st.tabs(["💼 LinkedIn", "🐦 Twitter/X", "📸 Instagram"])

    with tab_li:
        st.code(result.linkedin_post, language=None, wrap_lines=True)

    with tab_tw:
        if not result.twitter_thread:
            st.info("Thread generate nahi hua.")
        for i, tweet in enumerate(result.twitter_thread, 1):
            st.code(tweet, language=None, wrap_lines=True)
            n = len(tweet)
            if n > 280:
                st.error(f"Tweet {i}: {n}/280 (limit cross)")
            else:
                st.caption(f"Tweet {i}: {n}/280")

    with tab_ig:
        st.code(result.instagram_caption, language=None, wrap_lines=True)

    st.subheader("Hashtags")
    st.code(" ".join(result.hashtags), language=None)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sources")
        for s in result.sources:
            st.write(f"- {s}")
    with col2:
        st.subheader("Tools used")
        st.write(", ".join(result.tools_used) or "None")

    if st.button("💾 Save to file"):
        st.success(save_to_txt(result.model_dump_json(indent=2)))