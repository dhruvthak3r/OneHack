import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig

async def crawler():
    browser_config = BrowserConfig(
        headless=True,
        java_script_enabled=True,
    )
    js_script = window.scrollTo(0, document.body.scrollHeight)
    browser_config.add_js_script(js_script)
    async with AsyncWebCrawler(config=browser_config) as crawler: 
     result = await crawler.arun("https://devfolio.co/hackathons/")
     print(result.markdown)
     

if __name__ == "__main__" :
   asyncio.run(crawler())

