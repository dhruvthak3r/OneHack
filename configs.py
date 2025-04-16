import os
from dotenv import load_dotenv
load_dotenv()

from models import ExtractSchema


from crawl4ai.extraction_strategy import LLMExtractionStrategy,JsonCssExtractionStrategy
from crawl4ai import LLMConfig,BrowserConfig,CrawlerRunConfig,CacheMode


def get_LLMExtraction_strategy(instruction : str):

    llm_config = LLMConfig(
        provider = "groq/deepseek-r1-distill-llama-70b",
        api_token = os.getenv("GROQ_API_KEY"),
        temprature=1,
        max_tokens=4096,
    )

    llm_extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        instruction=instruction,
        schema=ExtractSchema.model_json_schema(),
        extraction_type="schema",
        input_format="markdown",
        verbose=True
    )

    return llm_extraction_strategy


def get_browser_config():
   
   Browser_config = BrowserConfig(
        headless=False,
        browser_type="chromium",
        cookies=None
    )
   
   return Browser_config


def get_crawler_run_config(instruction : str):
    crawler_run_config = CrawlerRunConfig(
        extraction_strategy=get_LLMExtraction_strategy(instruction),
        stream=True,
        cache_mode=CacheMode.BYPASS,
        js_code="window.scrollTo(0, document.body.scrollHeight);",
        scan_full_page = True,
        scroll_delay=1.2,
        adjust_viewport_to_content=True,
        verbose=True,
        log_console=True,
    )

    return crawler_run_config



    