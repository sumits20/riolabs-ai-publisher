import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from graph_builder import build_graph

st.title("Riolabs Content Agent")

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"]
)

graph = build_graph(llm)

user_input = st.text_input("Ask something")

if st.button("Run") and user_input:
    result = graph.invoke({
        "messages": [HumanMessage(content=user_input)]
    })

    for msg in result["messages"]:
        st.write(msg.__class__.__name__, ":", msg.content)
