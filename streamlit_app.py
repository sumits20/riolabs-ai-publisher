import streamlit as st
from tools.wordpress_tools import get_recent_posts

st.title("Riolabs Content Agent")

if st.button("Load recent posts"):
    posts = get_recent_posts(5)
    st.write(posts)
