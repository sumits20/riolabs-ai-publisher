from tools.wordpress_tools import get_recent_posts_tool
import streamlit as st

if st.button("Test tool"):
    st.write(get_recent_posts_tool.invoke({}))
