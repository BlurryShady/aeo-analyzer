from bs4 import BeautifulSoup


def analyze_content(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    headings_data = []
    headings = soup.find_all(["h1", "h2", "h3"])
    for heading in headings:
        headings_data.append({"level": heading.name, "text": heading.get_text()})


    schema_tags = soup.find_all("script", {"type": "application/ld+json"})
    schema_found = bool(schema_tags)

    h1_count = len([h for h in headings_data if h["level"] == "h1"])
    h2_count = len([h for h in headings_data if h["level"] == "h2"])
    h3_count = len([h for h in headings_data if h["level"] == "h3"])

    return {
        "headings": headings_data,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "h3_count": h3_count,
        "schema_found": schema_found,
        "schema_message": "Schema is empty. Schema should be created for AI to analyze better on the website." if not schema_found else None
    }



#Test section for only this file.
if __name__ == "__main__":
    import asyncio
    from ..fetcher import fetch_url

    async def test():
        result = await fetch_url("https://blog.blurryshady.dev")
        analysis = analyze_content(result["html"])
        print(analysis["headings"])
        print(analysis["h1_count"])
        print(analysis["h2_count"])
        print(analysis["h3_count"])
        print(analysis["schema_found"])
        print(analysis["schema_message"])

    asyncio.run(test())