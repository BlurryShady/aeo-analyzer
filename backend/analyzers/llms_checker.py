from urllib.parse import urlparse
from ..fetcher import fetch_url
import re


async def fetch_llms_txt(url: str) -> dict:
    parsed = urlparse(url)
    llms_url = f"{parsed.scheme}://{parsed.netloc}/llms.txt"

    result = await fetch_url(llms_url)

    if result["success"] and result["status_code"] == 200:
        return {
            "exists": True,
            "content": result["html"],
            "llms_url": llms_url
        }
    else:
        return {
            "exists": False,
            "content": "",
            "llms_url": llms_url
        }


def parse_llm_txt(content: str) -> dict:
    """
    Evaluates the quality of an llms.txt file using structural signals:
    presence of headers, presence of markdown links, and overall length.

    Returns a dict with raw counts and an overall quality assessment.

    This part only checks url existance. Does not check link itself.
    """
    lines = content.splitlines()

    header_count = 0
    link_count = 0

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("#"):
            header_count += 1

        if re.search(r"\[.+?\]\(.+?\)", stripped_line):
            link_count += 1

    word_count = len(content.split())

    return {
        "header_count": header_count,
        "link_count": link_count,
        "word_count": word_count
    }


def assess_llm_txt_quality(stats: dict) -> dict:
    """
    Scores an llms.txt file's structure across three independent dimensions:
    headers, links, and overall length. Each dimension is scored separately
    rather than mathematically combined (e.g. words-per-header). I've analyzed few llms.txt files and this scoring system is great way to start this project.

    Each dimension returns both a "status" (for code/logic to branch on)
    and a "message" (human-readable, includes the actual numbers, for
    display on the dashboard).
    """
    header_count = stats["header_count"]
    link_count = stats["link_count"]
    word_count = stats["word_count"]

    # Header dimension
    if header_count == 0:
        header_status = "missing"
        header_message = "No headers found. Add at least 3 section headers (##) to organize your content."
    elif header_count <= 3:
        header_status = "minimal"
        header_message = f"Current header count is {header_count}, should be at least 4 for well-organized content."
    else:
        header_status = "strong"
        header_message = f"Current header count is {header_count}. Well-structured."

    # Link dimension
    if link_count == 0:
        link_status = "missing"
        link_message = "No links found. Add links to guide agents to your most important pages."
    elif link_count <= 3:
        link_status = "minimal"
        link_message = f"Current link count is {link_count}, should be at least 4 to meaningfully guide agents."
    else:
        link_status = "strong"
        link_message = f"Current link count is {link_count}. Good navigation coverage."

    # Length dimension
    if word_count < 20:
        length_status = "missing"
        length_message = f"Current word count is {word_count}, which is too short to convey meaningful information."
    else:
        length_status = "sufficient"
        length_message = f"Current word count is {word_count}. Sufficient length."

    return {
        "header_status": header_status,
        "header_message": header_message,
        "link_status": link_status,
        "link_message": link_message,
        "length_status": length_status,
        "length_message": length_message
    }


# Manual test block run this file to test.
# correctly counts headers, links and words in a sample llms.txt.
if __name__ == "__main__":
    sample_llms_txt = """
# My Portfolio

A full-stack developer site showcasing projects.

## Projects
- [Blog Project](https://blog.blurryshady.dev))
- [Marvel Rivals Team Builder](https://rivals.blurryshady.dev)

## Contact
- [Get in touch](https://blurryshady.dev/contact) (This one doesn't exist.)
"""

    result = parse_llm_txt(sample_llms_txt)
    print(result)

    quality = assess_llm_txt_quality(result)
    print(quality)