from .analyzers.token_analyzer import analyze_tokens
from .analyzers.content_analyzer import analyze_content
from .analyzers.llms_checker import assess_llm_txt_quality, parse_llm_txt, fetch_llms_txt
from .analyzers.robots_checker import parse_robots_txt, fetch_robots_txt
from .fetcher import fetch_url, extract_content



async def generate_recommendations(url: str) -> dict:
    result = await fetch_url(url)

    token_result = await analyze_tokens(url)
    content_result = analyze_content(result["html"])
    robots_fetch = await fetch_robots_txt(url)
    robots_result = parse_robots_txt(robots_fetch["content"])
    llms_fetch = await fetch_llms_txt(url)
    llms_stats = parse_llm_txt(llms_fetch["content"])
    llms_result = assess_llm_txt_quality(llms_stats)


    recommendations = []

    for agent, status in robots_result.items():
        if status == "blocked":
            recommendations.append(
                {
                "priority": "high",
                "category": "robots",
                "issue": f"{agent} is fully blocked in robots.txt",
                "fix": "Remove or modify the Disallow: / rule for this agent"
                }
            )
        elif status == "partially_blocked":
            recommendations.append(
                {
                "priority": "medium",
                "category": "robots",
                "issue": f"{agent} is partially blocked in robots.txt",
                "fix": "If it is not intentional, consider modifying the Disallow rules to allow access to important pages"
                }
            )
        elif status == "allowed_no_rules_wildcard_blocks":
            recommendations.append(
                {
                "priority": "low",
                "category": "robots",
                "issue": f"{agent} is allowed in robots.txt but there are wildcard rules that may block access to some pages",
                "fix": "Review the Disallow rules and ensure they do not unintentionally block important pages"
                }
            )


    if llms_result["header_status"] == "missing":
        recommendations.append({
            "priority": "high",
            "category": "llms",
            "issue": llms_result["header_message"],
            "fix": "Add context to llms"
            }
        )
    elif llms_result["header_status"] == "minimal":
        recommendations.append({
            "priority": "medium",
            "category": "llms",
            "issue": llms_result["header_message"],
            "fix": "If it is not intended, consider adding more context to llms"
            }
        )


    if llms_result["link_status"] == "missing":
        recommendations.append({
            "priority": "high",
            "category": "llms",
            "issue": llms_result["link_message"],
            "fix": "Add links to llms so agents can have a link to give to user"
            }
        )
    elif llms_result["link_status"] == "minimal":
        recommendations.append({
            "priority": "medium",
            "category": "llms",
            "issue": llms_result["link_message"],
            "fix": "There can be more links on llms for agents to read"      
            }
        )
    
    if llms_result["length_status"] == "missing":
        recommendations.append({
            "priority": "high",
            "category": "llms",
            "issue": llms_result["length_message"],
            "fix": "Add context to llms"
            }
        )


    if token_result["openai_token_count"] < 200:
         recommendations.append({
            "priority": "medium",
            "category": "tokens",
            "issue": "Very little content, AI agent may not find enough useful information",
            "fix": "Add more content to the site for AI to understand better"
            }
        )
    elif 10000 < token_result["openai_token_count"] < 50000:
         recommendations.append({
            "priority": "low",
            "category": "tokens",
            "issue": "Page is content heavy, ensure content is well-structured and not repetitive",
            "fix": "Go over the site to make it a bit more simple"
            }
        )
    elif token_result["openai_token_count"] > 50000:
         recommendations.append({
            "priority": "medium",
            "category": "tokens",
            "issue": "Page is extremely long, AI agents may struggle to process all content effectively",
            "fix": "Consider splitting long content into multiple focused pages, removing repetitive boilerplate and ensuring each page covers one clear topic."
            }
        )


    if not content_result["schema_found"]:
         recommendations.append({
            "priority": "high",
            "category": "content",
            "issue": "There is no schema on the website",
            "fix": "Lack of schema means there is no structure for agent to read which is important for healthy read of an agent, add schema to the website"
            }
        )
   
    if content_result["h1_count"] == 0:
        recommendations.append({
            "priority": "medium",
            "category": "content",
            "issue": "There is no H1 tag on the website",
            "fix": "Add an H1 tag to the website to provide a clear and concise heading for the page"
            }
        )
    elif content_result["h1_count"] > 1:
        recommendations.append({
            "priority": "medium",
            "category": "content",
            "issue": "There are multiple H1 tags on the website",
            "fix": "Ensure there is only one H1 tag per page to maintain proper heading hierarchy and improve accessibility"
            }
        )

    if 0 < content_result["h2_count"] < 3:
        recommendations.append({
            "priority": "medium",
            "category": "content",
            "issue": "There are only a few H2 tags on the website",
            "fix": "Consider adding more H2 tags to provide better structure and organization for the content"
            }
        )
    elif content_result["h2_count"] > 40:
        recommendations.append({
            "priority": "low",
            "category": "content",
            "issue": "There are too many H2 tags on the website",
            "fix": "Ensure that H2 tags are used appropriately and not excessively, as it may lead to confusion and poor user experience"
            }
        )


    return {
    "url": url,
    "recommendations": recommendations,
    "raw": {
        "robots": robots_result,
        "llms": llms_result,
        "tokens": token_result,
        "content": content_result
    }
    }



#Test section for only this file.
if __name__ == "__main__":
    import asyncio

    async def test():
        result = await generate_recommendations("https://blog.blurryshady.dev")
        print(result["url"])
        for rec in result["recommendations"]:
            print(rec)

    asyncio.run(test())