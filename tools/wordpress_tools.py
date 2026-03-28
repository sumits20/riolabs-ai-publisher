import requests


def get_recent_posts(limit: int = 10) -> list[dict]:
    url = "https://riolabs.in/wp-json/wp/v2/posts"
    params = {
        "per_page": limit,
        "_fields": "id,date,slug,title,link"
    }

    response = requests.get(url, params=params, timeout=20)
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
