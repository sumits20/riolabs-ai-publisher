import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from tools.tavily_research import research_topic

from graph_builder import build_graph

st.title("Riolabs Content Agent")

import requests
from requests.auth import HTTPBasicAuth

if st.button("Test authenticated WP direct"):
    try:
        r = requests.get(
            "https://riolabs.in/wp-json/wp/v2/posts",
            params={"per_page": 3, "_fields": "id,title,link"},
            auth=HTTPBasicAuth(
                st.secrets["WORDPRESS_USERNAME"],
                st.secrets["WORDPRESS_APP_PASSWORD"]
            ),
            headers={"User-Agent": "Mozilla/5.0 (compatible; RiolabsContentAgent/1.0)"},
            timeout=(15, 45),
        )
        st.write("Status code:", r.status_code)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

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
