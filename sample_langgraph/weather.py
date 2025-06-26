from mcp.server.fastmcp import FastMCP
import re
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

llm = ChatGroq(
    temperature=0.3,  # Reduced temperature for more consistent output
    model_name="llama-3.3-70b-versatile"
)

mcp = FastMCP("Weather")

search_tool = DuckDuckGoSearchRun()


@mcp.tool()
async def get_weather(location:str)->dict:
    """Get the weather of location using DuckDuckGo Search and extract relevant information."""
    try:
        search_query = f"weather forecast {location}"
        search_results = search_tool.run(search_query)

        print("Raw search results:", search_results[:200], "...")

        # First try direct regex extraction from search results
        # Extract temperature
        temp_patterns = [
            r'temperature of (\d+)°?[CF]',  # "temperature of 29°C"
            r'(\d+)°[CF]',                  # "29°C"
            r'(\d+) ?degrees?'              # "29 degrees"
        ]

        current_temp = "Not available"
        for pattern in temp_patterns:
            temp_match = re.search(pattern, search_results, re.IGNORECASE)
            if temp_match:
                current_temp = f"{temp_match.group(1)}°C"
                break

        # Extract conditions
        conditions = "Variable"
        condition_keywords = {
            'mist': 'Misty',
            'fog': 'Foggy',
            'rain': 'Rainy',
            'shower': 'Showers',
            'overcast': 'Overcast',
            'cloudy': 'Cloudy',
            'sunny': 'Sunny',
            'clear': 'Clear',
            'partly cloudy': 'Partly Cloudy'
        }

        search_lower = search_results.lower()
        for keyword, condition in condition_keywords.items():
            if keyword in search_lower:
                conditions = condition
                break

        # Extract forecast info
        forecast = "Variable conditions expected"
        if 'shower' in search_lower or 'rain' in search_lower:
            forecast = "Expect rain or showers"
        elif 'overcast' in search_lower:
            forecast = "Overcast skies expected"
        elif 'mist' in search_lower:
            forecast = "Misty conditions likely"

        print(f"Direct extraction: Temp={current_temp}, Conditions={conditions}")

        # Try LLM extraction as backup only if direct extraction failed
        if current_temp == "Not available":
            print("Trying LLM extraction as backup...")

            weather_extraction_prompt = ChatPromptTemplate.from_messages([
                ("system", """Look at the weather search results and extract:
                1. Current temperature (just the number and unit like "29°C")
                2. Weather condition (one word like Sunny, Cloudy, Rainy, Misty)
                3. Brief forecast (max 10 words)

                Return format:
                Temperature: [temp]
                Condition: [condition]
                Forecast: [forecast]"""),
                ("user", "Weather data: {text}")
            ])

            try:
                extraction_response = llm.invoke(
                    weather_extraction_prompt.format_messages(text=search_results[:1000])
                )

                llm_response = extraction_response.content
                print(f"LLM response: {llm_response}")

                # Parse LLM response
                temp_match = re.search(r'Temperature:\s*([^\n]+)', llm_response)
                cond_match = re.search(r'Condition:\s*([^\n]+)', llm_response)
                fore_match = re.search(r'Forecast:\s*([^\n]+)', llm_response)

                if temp_match:
                    current_temp = temp_match.group(1).strip()
                if cond_match:
                    conditions = cond_match.group(1).strip()
                if fore_match:
                    forecast = fore_match.group(1).strip()

            except Exception as llm_error:
                print(f"LLM extraction failed: {llm_error}")

        return {
            "city": location,
            "summary": f"Weather for {location}: {current_temp}, {conditions}",
            "current_temp": current_temp,
            "conditions": conditions,
            "forecast": forecast,
            "raw_search_results": search_results[:500] + "..." if len(search_results) > 500 else search_results
        }

    except Exception as e:
        print(f"Weather fetch error: {e}")
        return {
            "city": location,
            "summary": f"Weather information unavailable for {location}",
            "current_temp": "Not available",
            "conditions": "Check local weather",
            "forecast": "Please check local weather services",
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run(transport='streamable-http')