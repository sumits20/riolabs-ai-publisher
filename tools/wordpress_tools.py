import requests
from langchain_core.tools import tool

@tool
def get_recent_posts_tool(limit: int = 10) -> str:
    """
    Fetch recent blog posts from the website.
    Returns titles and links of recent posts.
    """
    posts = get_recent_posts(limit)

    formatted = "\n".join([
        f"{p['title']} ({p['link']})"
        for p in posts
    ])

    return formatted
