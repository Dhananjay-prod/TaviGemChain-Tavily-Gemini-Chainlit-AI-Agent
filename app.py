import os
from google import genai
import chainlit as cl
from tavily import TavilyClient
import trafilatura
import asyncio
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    if not GOOGLE_API_KEY or not TAVILY_API_KEY:
        raise ValueError("Missing API keys. Please check your .env file")
    
    client = genai.Client(api_key=GOOGLE_API_KEY)
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    
except Exception as e:
    logger.error(f"Failed to initialize API clients: {e}")
    raise

def get_additional_data(message: str, max_results: int = 5) -> str:
    try:
        response = tavily_client.search(message, max_results=max_results)
        urls = [item["url"] for item in response.get("results", []) if item.get("url")]
        
        if not urls:
            logger.warning("No URLs found for the query")
            return ""
        
        logger.info(f"Found {len(urls)} URLs to scrape")
        return webscrap(urls)
    
    except Exception as e:
        logger.error(f"Error in get_additional_data: {e}")
        return ""

def webscrap(urls: List[str]) -> str:
    main_contents = []
    successful_scrapes = 0
    
    for url in urls:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                extracted = trafilatura.extract(downloaded)
                if extracted:
                    main_contents.append(extracted)
                    successful_scrapes += 1
                    logger.info(f"Successfully scraped: {url}")
        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            continue
    
    logger.info(f"Successfully scraped {successful_scrapes}/{len(urls)} URLs")
    return "\n\n---\n\n".join(main_contents)

@cl.on_message
async def main(message: cl.Message):
    try:
        thinking_msg = cl.Message(content="🔍 Searching for relevant information...")
        await thinking_msg.send()
        
        additional_data = await cl.make_async(get_additional_data)(message.content)
        
        await thinking_msg.remove()
        
        if additional_data:
            prompt = (
                f"User Query: {message.content}\n\n"
                f"Context from web search:\n{additional_data[:8000]}\n\n"
                "Please provide a comprehensive answer based on the above context. "
                "If the context is relevant, use it to enhance your response. "
                "Format your response with clear sections and markdown where appropriate."
            )
        else:
            prompt = (
                f"User Query: {message.content}\n\n"
                "Note: No additional web context was found. "
                "Please provide the best answer based on your knowledge."
            )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt]
        )
        
        if not response.candidates:
            raise ValueError("No response generated from the model")
        
        full_text = response.candidates[0].content.parts[0].text
        
        msg = cl.Message(content="")
        await msg.send()
        
        chunk_size = 5
        for i in range(0, len(full_text), chunk_size):
            chunk = full_text[i:i + chunk_size]
            await msg.stream_token(chunk)
            await asyncio.sleep(0.001)
        
        await msg.update()
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        error_message = (
            "❌ Sorry, an error occurred while processing your request.\n\n"
            f"Error details: `{str(e)}`\n\n"
            "Please try again or rephrase your question."
        )
        await cl.Message(content=error_message).send()

if __name__ == "__main__":
    cl.run()
