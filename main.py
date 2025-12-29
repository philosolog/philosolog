import json
import pathlib
import re
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content: str, marker: str, chunk: str) -> str:
    """Replace content between marker comments in the README."""
    pattern = re.compile(
        rf"<!-- {marker} starts -->.*<!-- {marker} ends -->",
        re.DOTALL,
    )
    replacement = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return pattern.sub(replacement, content)


def fetch_blog_posts(limit: int = 3) -> list[dict[str, Any]]:
    """Fetch latest blog posts from the philosolog.com API."""
    url = f"https://philosolog.com/api/posts?limit={limit}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def format_posts_markdown(posts: list[dict[str, Any]]) -> str:
    """Format blog posts as a markdown list with date, title, and description."""
    entries = []
    for post in posts:
        title = post["title"]
        url = post["url"]
        date = post["date"]
        description = post["description"]
        entries.append(f"- **{date}** — [{title}]({url})\\\n  {description}")
    return "\n".join(entries)


if __name__ == "__main__":
    readme_path = ROOT / "README.md"
    readme_contents = readme_path.read_text(encoding="utf-8")
    posts = fetch_blog_posts(limit=3)
    posts_md = format_posts_markdown(posts)
    updated = replace_chunk(readme_contents, "blog", posts_md)

    readme_path.write_text(updated, encoding="utf-8")