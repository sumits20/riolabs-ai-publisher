import requests
from langchain_core.tools import tool


def get_recent_posts(limit: int = 10) -> list[dict]:
    url = "https://riolabs.in/wp-json/wp/v2/posts"
    params = {
        "per_page": limit,
        "_fields": "id,date,slug,title,link"
    }

    response = requests.get(url, params=params, timeout=(10, 30))
    response.raise_for_status()

    posts = response.json()

    cleaned_posts = []
    for post in posts:
        cleaned_posts.append({
            "id": post.get("id"),
            "date": post.get("date"),
            "slug": post.get("slug"),
            "title": post.get("title", {}).get("rendered", ""),
            "link": post.get("link")
        })

    return cleaned_posts


@tool
def get_recent_posts_tool(limit: int = 10) -> str:
    """
    Fetch recent posts already published on the user's own WordPress website.
    Use this tool when you need to know what topics already exist on the user's blog,
    avoid duplicate ideas, compare against existing content, or understand what has already been published.
    Returns recent post titles and links.
    """
    try:
        posts = get_recent_posts(limit)

        if not posts:
            return "No recent posts were found on the website."

        return "\n".join(
            f"{p['title']} ({p['link']})"
            for p in posts
        )

    except requests.exceptions.ConnectTimeout:
        return "Could not connect to the WordPress website in time. The site may be slow or temporarily unreachable."

    except requests.exceptions.ReadTimeout:
        return "The WordPress website took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"Failed to fetch recent posts from WordPress: {str(e)}"
