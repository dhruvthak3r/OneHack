import asyncio
import os

from config import get_llmextraction_strategy

from dotenv import load_dotenv
load_dotenv()

from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode

from playwright.async_api import Page,BrowserContext
async def crawler():
    Browser_config = BrowserConfig(
        headless=False,
        browser_type="chromium",
        cookies=None
    )
    
    crawler_config = CrawlerRunConfig(
       cache_mode=CacheMode.BYPASS,
       js_code="window.scrollTo(0, document.body.scrollHeight);",
       scan_full_page = True,
       scroll_delay=1.2,
       adjust_viewport_to_content=True,
       extraction_strategy=get_llmextraction_strategy(),
       verbose=False
    )
    
    async with AsyncWebCrawler(config=Browser_config) as crawler:
     await crawler.awarmup()
     result = await crawler.arun("https://devfolio.co/hackathons/open",config=crawler_config)
     print("js : " + str(result.js_execution_result))
     print("error :" + str(result.error_message))
     print("extracted content " + str(result.extracted_content))

     

if __name__ == "__main__" :
   asyncio.run(crawler())

