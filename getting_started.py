import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode

async def crawler():
    Browser_config = BrowserConfig(
        headless=False,
        browser_type="Edge",
        cookies=None
    )
    crawler_config = CrawlerRunConfig(
       cache_mode=CacheMode.BYPASS,
       js_code="window.scrollTo(0, document.body.scrollHeight);",
       scan_full_page = True,
       scroll_delay=0.5,
       adjust_viewport_to_content=True
    )
    async with AsyncWebCrawler(config=Browser_config) as crawler:
     result = await crawler.arun("https://devfolio.co/hackathons/open",config=crawler_config)
     print(result.status_code)
     print(result.success)
     print(result.markdown)
     

if __name__ == "__main__" :
   asyncio.run(crawler())

