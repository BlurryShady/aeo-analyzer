import httpx
import time

# Mimic a generic AI agent user-agent for baseline fetching.
AGENT_USER_AGENT = "AEO-Analyzer/1.0 (+https://github.com/BlurryShady/aeo-analyzer)"


async def fetch_url(url: str) -> dict:
    """
    Fetches a URL the way a basic AI agent/crawler would:
    raw HTTP GET, no JavaScript usage.

    Returns a dict with status, headers, html content and timing.

    This part is the core of fetching logic of AEO Analyzer.

    Unlike "requests" "httpx" works asynchronously which is perfect for my app.
    """
    headers = {
        "User-Agent": AGENT_USER_AGENT
    }

    start_time = time.time()

    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            elapsed = time.time() - start_time

            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "html": response.text,
                "final_url": str(response.url),
                "elapsed_seconds": round(elapsed, 3),
                "error": None
            }

        except httpx.RequestError as e:
            elapsed = time.time() - start_time
            return {
                "success": False,
                "status_code": None,
                "headers": {},
                "html": "",
                "final_url": url,
                "elapsed_seconds": round(elapsed, 3),
                "error": str(e)
            }




from bs4 import BeautifulSoup


def extract_content(html: str) -> dict:
    """
    Parses raw HTML and extracts clean, readable text.
    Also estimates how much of the page depends on JavaScript,
    based on the ratio of raw HTML size to actual readable text.

    Returns a dict with clean text, word count, and a JS-dependency signal.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    clean_text = soup.get_text(separator=" ", strip=True)
    word_count = len(clean_text.split())

    html_length = len(html)
    text_length = len(clean_text)

    # Avoid divide-by-zero on completely empty pages.
    text_to_html_ratio = (text_length / html_length) if html_length > 0 else 0

    # Heuristic: if the page has a lot of raw HTML but very little.
    # of it is actual readable text, real content is likely injected by JS.
    likely_js_dependent = html_length > 5000 and text_to_html_ratio < 0.05

    return {
        "clean_text": clean_text,
        "word_count": word_count,
        "html_length": html_length,
        "text_to_html_ratio": round(text_to_html_ratio, 4),
        "likely_js_dependent": likely_js_dependent
    }



#Temporary Test Part. Uncomment and use this to test fetcher.
""" if __name__ == "__main__":
    import asyncio

    async def test():
        result = await fetch_url("https://www.example.com")
        print("Success:", result["success"])
        print("Status code:", result["status_code"])
        print("Final URL:", result["final_url"])
        print("Elapsed:", result["elapsed_seconds"], "seconds")
        print("HTML length:", len(result["html"]))

        content = extract_content(result["html"])
        print("Word count:", content["word_count"])
        print("Likely JS-dependent:", content["likely_js_dependent"])
        print("First 200 chars of clean text:", content["clean_text"][:200])

    asyncio.run(test()) """