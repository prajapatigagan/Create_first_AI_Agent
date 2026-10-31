# import streamlit as st

# from main import agent, to_structured, get_tools_used
# from tools import save_to_txt

# st.set_page_config(page_title="AI Research Assistant", page_icon="🔎", layout="wide")
# st.title("🔎 AI Research Assistant")

# if "history" not in st.session_state:
#     st.session_state.history = []

# query = st.text_input("Kya research karna hai?", placeholder="e.g. Capital of India")

# if st.button("Research karo", type="primary") and query.strip():
#     try:
#         with st.spinner("Research chal rahi hai..."):
#             raw = agent.invoke({"messages": [{"role": "user", "content": query}]})
#             answer = raw["messages"][-1].content
#             result = to_structured(query, answer)
#             result.tools_used = get_tools_used(raw["messages"])
#             save_to_txt(result.model_dump_json(indent=2))
#         st.session_state.history.insert(0, result)
#     except Exception as e:
#         st.error(f"Error: {e}")


# def show(result):
#     st.header(result.topic)
#     st.markdown(result.summary)

#     key_points = getattr(result, "key_points", [])
#     if key_points:
#         st.subheader("Key points")
#         for p in key_points:
#             st.markdown(f"- {p}")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Sources")
#         for s in result.sources or ["No sources"]:
#             st.markdown(f"- {s}")
#     with col2:
#         st.subheader("Tools used")
#         for t in result.tools_used or ["None"]:
#             st.markdown(f"- `{t}`")

#     st.download_button(
#         "JSON download karo",
#         result.model_dump_json(indent=2),
#         file_name=f"{result.topic[:30]}.json",
#         mime="application/json",
#         key=f"dl_{id(result)}",
#     )


# if st.session_state.history:
#     show(st.session_state.history[0])

#     if len(st.session_state.history) > 1:
#         st.divider()
#         st.subheader("Pichli researches")
#         for r in st.session_state.history[1:]:
#             with st.expander(r.topic):
#                 show(r)


