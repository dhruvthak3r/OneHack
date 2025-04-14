import os
from dotenv import load_dotenv
load_dotenv()

from models import ExtractSchema
from pydantic.json_schema import GenerateJsonSchema

from crawl4ai.extraction_strategy import LLMExtractionStrategy,JsonCssExtractionStrategy
from crawl4ai import LLMConfig
from crawl4ai.content_filter_strategy import LLMContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def get_Markdown_generator():

    llm_config = LLMConfig(
        provider = "groq/deepseek-r1-distill-llama-70b",
        api_token = os.getenv("GROQ_API_KEY"),
        temprature=1,
        max_tokens=2048,
    )

    filter = LLMContentFilter(
        llm_config=llm_config,
        instruction="""
           Focus on Extracting relevant infromation about hackathons from the stage
           Include:
              - name of the hackathon
              - description of the hackathon
              - start date of the hackathon
              - end date of the hackathon
              - link to the hackathon
            Exlude:
                - irrelevant information
                - any other information that is not related to hackathons
                - footer content
                - sidebars
                - navigation elements
            Format the output as clean markdown with proper code blocks and headers.
          """,
           chunk_token_threshold=2048,
           word_token_rate=0.5,
    )

    llm_content_filter = DefaultMarkdownGenerator(
        content_filter=filter,
    )
    return llm_content_filter

def get_jsoncss_extraction_strategy():
    json_css_extraction_strategy = JsonCssExtractionStrategy(
    )
    return json_css_extraction_strategy

if __name__ == "__main__":
    get_Markdown_generator()
