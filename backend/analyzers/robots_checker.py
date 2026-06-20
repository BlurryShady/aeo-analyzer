# Known AI crawler/agent user-agent names found in robots.txt files. I will add more as I learn more agents and my app itself adds it to database as it's used more and more.
KNOWN_AI_AGENTS = [
    "GPTBot",           # OpenAI
    "ChatGPT-User",      # OpenAI (when ChatGPT browses on a user's behalf)
    "ClaudeBot",          # Anthropic
    "Claude-Web",         # Anthropic (older)
    "anthropic-ai",       # Anthropic
    "Google-Extended",   # Google (Gemini/Bard training)
    "CCBot",              # Common Crawl (used by many AI training sets)
    "PerplexityBot",      # Perplexity AI
    "Bytespider",         # ByteDance/TikTok AI
    "Amazonbot",          # Amazon (Alexa/AI)
    "Applebot-Extended",  # Apple AI
]



from urllib.parse import urlparse
from ..fetcher import fetch_url


async def fetch_robots_txt(url: str) -> dict:
    """
    Constructs the robots.txt URL for a given site and fetches it,
    reusing the core fetch_url() function from fetcher.py.

    Returns a dict with the raw robots.txt content (or empty if not found)
    and whether the fetch succeeded.
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    result = await fetch_url(robots_url)

    if result["success"] and result["status_code"] == 200:
        return {
            "exists": True,
            "content": result["html"],
            "robots_url": robots_url
        }
    else:
        return {
            "exists": False,
            "content": "",
            "robots_url": robots_url
        }



def parse_robots_txt(content: str) -> dict:
    lines = content.splitlines()
    
    agent_rules = {}
    current_agents = []
    expecting_new_group = True  # tracks whether we're still collecting agent names, important for Python's way of reading line by line. Without this app wouldn't work with multiple agents.

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("user-agent:"):
            agent_name = line.split(":", 1)[1].strip()

            if expecting_new_group:
                current_agents.append(agent_name)
            else:
                # a new group is starting fresh
                current_agents = [agent_name]
                expecting_new_group = True

            if agent_name not in agent_rules:
                agent_rules[agent_name] = []

        elif line.lower().startswith("disallow:") and current_agents:
            path = line.split(":", 1)[1].strip()
            for agent in current_agents:
                agent_rules[agent].append(path)
            expecting_new_group = False
    
    # Now check each known AI agent against the parsed rules.
    results = {}

    for agent in KNOWN_AI_AGENTS:
        if agent in agent_rules:
            disallow_paths = agent_rules[agent]
            if "/" in disallow_paths:
                results[agent] = "blocked"
            elif len(disallow_paths) > 0:
                results[agent] = "partially_blocked"
            else:
                results[agent] = "allowed"
        elif "*" in agent_rules:
            disallow_paths = agent_rules["*"]
            if "/" in disallow_paths:
                results[agent] = "blocked"
            elif len(disallow_paths) > 0:
                results[agent] = "partially_blocked"
            else:
                results[agent] = "allowed"
        else:
            results[agent] = "not_mentioned"

    return results


#Test part for robots.txt parsing. Same as fetcher.py test.
if __name__ == "__main__":
    sample_robots_txt = """
User-agent: GPTBot
User-agent: ClaudeBot
Disallow: /

User-agent: PerplexityBot
Disallow: /private/

User-agent: *
Disallow: /admin/
"""

    results = parse_robots_txt(sample_robots_txt)

    for agent, status in results.items():
        print(f"{agent}: {status}")