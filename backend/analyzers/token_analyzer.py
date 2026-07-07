from unittest import result

from ..fetcher import fetch_url
from ..fetcher import extract_content
import tiktoken
import anthropic



client = anthropic.AsyncAnthropic()



async def analyze_tokens(url: str) -> dict:
    result = await fetch_url(url)
    content = extract_content(result["html"])
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content["clean_text"])
    openai_token_count = len(tokens)
    try:
        response = await client.messages.count_tokens(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": content["clean_text"]}]
        )
        claude_token_count = response.input_tokens
    except Exception as e:
        claude_token_count = None
    
    return {
        "openai_token_count": openai_token_count,
        "claude_token_count": claude_token_count,
        "minimum_usage": int(openai_token_count * 0.85),
        "maximum_usage": int(openai_token_count * 1.15),
        "word_count": content["word_count"],
        "js_dependent": content["likely_js_dependent"],
        "disclaimer": "This website uses JavaScript so token usage might be higher than estimated." if content["likely_js_dependent"] else None
    }


#Test section for only this file.
if __name__ == "__main__":
    import asyncio

    async def test():
        result = await analyze_tokens("https://blog.blurryshady.dev")
        print(result["openai_token_count"])
        print(result["claude_token_count"])
        print(result["minimum_usage"])
        print(result["maximum_usage"])
        print(result["word_count"])
        print(result["js_dependent"])

    asyncio.run(test())