import asyncio
import os
import json

from config import get_Markdown_generator

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
       markdown_generator=get_Markdown_generator(),
       cache_mode=CacheMode.BYPASS,
       js_code="window.scrollTo(0, document.body.scrollHeight);",
       scan_full_page = True,
       scroll_delay=1.2,
       adjust_viewport_to_content=True,
       verbose=True,
       log_console=True,
    )
    async with AsyncWebCrawler(config=Browser_config) as crawler:
        await crawler.awarmup()
        result = await crawler.arun("https://devfolio.co/hackathons/open", config=crawler_config)
        print(result.status_code)
        print(result.markdown.fit_markdown)
     
if __name__ == "__main__" :
   asyncio.run(crawler())

