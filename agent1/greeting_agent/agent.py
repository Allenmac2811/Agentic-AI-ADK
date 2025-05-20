import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search
import requests

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

def search_linkedin_profile(name: str) -> dict:
    """Searches for a person on LinkedIn and returns their profile summary.

    Args:
        name (str): The full name of the person to search for.

    Returns:
        dict: A simulated LinkedIn profile summary or error message.
    """
    mock_profiles = {
        "john doe": {
            "name": "John Doe",
            "title": "Software Engineer at Google",
            "location": "San Francisco Bay Area",
            "linkedin_url": "https://www.linkedin.com/in/johndoe"
        },
        "jane smith": {
            "name": "Jane Smith",
            "title": "Product Manager at Amazon",
            "location": "Seattle, WA",
            "linkedin_url": "https://www.linkedin.com/in/janesmith"
        },
    }

    profile = mock_profiles.get(name.lower())
    if profile:
        return {"status": "success", "profile": profile}
    else:
        return {
            "status": "error",
            "error_message": f"No LinkedIn profile found for '{name}'."
        }

def get_wiki_summary(topic: str) -> dict:
    """Fetches a clean summary for the given topic from Wikipedia.

    Args:
        topic (str): The topic to look up (e.g., 'machine learning').

    Returns:
        dict: A dictionary with status and summary or error message.
    """
    # Clean and encode topic for URL
    topic_clean = topic.strip().replace(' ', '_')
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_clean}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Disambiguation page check
            if data.get("type") == "disambiguation":
                return {
                    "status": "warning",
                    "message": f"'{topic}' is a disambiguation page. Try being more specific.",
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
                }

            summary = data.get("extract", "No summary available.")
            return {
                "status": "success",
                "topic": data.get("title", topic),
                "summary": summary,
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }

        elif response.status_code == 404:
            return {
                "status": "error",
                "error_message": f"No Wikipedia article found for '{topic}'."
            }

        else:
            return {
                "status": "error",
                "error_message": f"Wikipedia request failed (HTTP {response.status_code})."
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Request failed: {str(e)}"
        }

def search_wikipedia(query: str) -> dict:
    """Searches Wikipedia for topics, people, or anything matching the query.

    Args:
        query (str): The search term or partial keyword.

    Returns:
        dict: A list of article titles that match the query.
    """
    url = f"https://en.wikipedia.org/w/rest.php/v1/search/title?q={query}&limit=5"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("pages", [])

            if not results:
                return {
                    "status": "error",
                    "error_message": f"No Wikipedia results found for '{query}'."
                }

            suggestions = [
                {
                    "title": page.get("title"),
                    "description": page.get("description", ""),
                    "url": f"https://en.wikipedia.org/wiki/{page.get('key')}"
                }
                for page in results
            ]

            return {
                "status": "success",
                "query": query,
                "results": suggestions
            }

        else:
            return {
                "status": "error",
                "error_message": f"Search failed (HTTP {response.status_code})."
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Search request failed: {str(e)}"
        }

def search_google_like(query: str) -> dict:
    """Performs a general web search using DuckDuckGo Instant Answer API.

    Args:
        query (str): The search term.

    Returns:
        dict: Summary or related topic links.
    """
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            abstract = data.get("Abstract")
            related_topics = data.get("RelatedTopics", [])

            if abstract:
                return {
                    "status": "success",
                    "source": "DuckDuckGo",
                    "summary": abstract,
                    "url": data.get("AbstractURL", "")
                }
            elif related_topics:
                suggestions = [
                    topic["Text"] for topic in related_topics[:5]
                    if isinstance(topic, dict) and "Text" in topic
                ]
                return {
                    "status": "partial",
                    "message": "No summary available, but related topics found.",
                    "related_topics": suggestions
                }
            else:
                return {
                    "status": "error",
                    "error_message": "No results found."
                }
        else:
            return {
                "status": "error",
                "error_message": f"DuckDuckGo request failed (HTTP {response.status_code})."
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Search failed: {str(e)}"
        }

def smart_topic_lookup(query: str) -> dict:
    """
    Smart topic lookup that combines web search and Wikipedia lookup.
    Works for people, companies, and concepts.
    """
    # First try a general web search
    print(f"🔍 Performing web search for: {query}")
    google_result = search_google_like(query)

    summary_from_web = None
    if google_result["status"] == "success":
        summary_from_web = google_result.get("summary")
    elif google_result["status"] == "partial":
        # Still use query as Wikipedia input
        print("⚠️ Web summary not found, using query directly for Wikipedia.")
    else:
        print("⚠️ Web search failed, continuing to Wikipedia.")

    # Step 2: Try Wikipedia search using query (not the summary)
    wiki_search_result = search_wikipedia(query)

    if wiki_search_result["status"] == "success" and wiki_search_result["results"]:
        top_topic = wiki_search_result["results"][0]["title"]
        print(f"📘 Found Wikipedia topic: {top_topic}")

        wiki_summary_result = get_wiki_summary(top_topic)

        return {
            "status": "success",
            "source_summary": summary_from_web,
            "wikipedia_topic": top_topic,
            "wikipedia_summary": wiki_summary_result.get("summary"),
            "wiki_url": wiki_summary_result.get("url")
        }

    else:
        return {
            "status": "error",
            "error_message": "Couldn't find relevant information on Wikipedia or web.",
            "source_summary": summary_from_web,
            "search_query_used": query
        }


root_agent = LlmAgent(
    # Use the latest stable Flash model identifier
    model="gemini-2.0-flash-lite",
    name="smart_lookup_agent",
    description="Agent that searches the web and Wikipedia to explain any topic.",
    instruction="You are a smart assistant who answers questions using both web search and Wikipedia lookups.",
    tools=[
        get_weather, 
        get_current_time,
        get_wiki_summary,
        search_wikipedia,
        search_google_like,
        smart_topic_lookup, 
        # google_search # Uncomment if you want to use Google Search
    ],
)