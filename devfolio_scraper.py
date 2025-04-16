import asyncio
import json
import time

from configs import get_browser_config,get_crawler_run_config

from crawl4ai import AsyncWebCrawler

async def get_name_and_links():
    Browser_config = get_browser_config()

    crawler_config = get_crawler_run_config(
        instruction="Extract all the hackathons from the page. The extracted data should be in JSON format. "
                    "The JSON format should be like this: "
                    '[{"name": "Hackathon Name", "link": "https://example.com"}]'
    )

    async with AsyncWebCrawler(config=Browser_config) as crawler:
        time.sleep(3)
        await crawler.awarmup()
        result = await crawler.arun("https://devfolio.co/hackathons/open", config=crawler_config)
        print(result.status_code)
        print(result.extracted_content)
        extraxted_content_json = json.loads(result.extracted_content)
        if extraxted_content_json[1]["error"] is not True:
          with open('devfolio_hackathons.json', 'w') as f:
            json.dump(extraxted_content_json, f, indent=2)

async def get_start_and_end_dates():
    Browser_config = get_browser_config()

    crawler_config = get_crawler_run_config(
        instruction="Extract all the hackathons from the page. The extracted data should be in JSON format. "
                    "The JSON format should be like this: "
                    '[{"start_date": "2023-01-01", "end_date": "2023-12-31"}]'
    )

    async with AsyncWebCrawler(config=Browser_config) as crawler:

        with open('devfolio_hackathons.json', 'r') as f:
            devfolio_info = json.load(f)
          
        links = [item["link"] for item in devfolio_info]

        for link in links:
            await crawler.awarmup()
            result = await crawler.arun(link, config=crawler_config)
            print(result.status_code)
            print(result.extracted_content)
            extraxted_content_json = json.loads(result.extracted_content)
            if extraxted_content_json[1]["error"] is not True:
                with open('devfolio_hackathons.json', 'w') as f:
                    json.dump(extraxted_content_json, f, indent=2)
       
if __name__ == "__main__" :
   asyncio.run(get_name_and_links())
   asyncio.run(get_start_and_end_dates())


