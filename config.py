import os
from dotenv import load_dotenv
load_dotenv()

from models import ExtractSchema
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import LLMConfig

def get_llmextraction_strategy():

    llm_config = LLMConfig(
        provider = "groq/deepseek-r1-distill-llama-70b",
        api_token = os.getenv("GROQ_API_KEY"),
        temprature=1,
        max_tokens=4096,
    )

    llm_extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        instruction="Extract all the hackathon information from the page including the name, description, start date, end date, Links to the hackathon events and any other relevant details.",
        schema= ExtractSchema.model_json_schema(),
        extraction_type="schema"
    )
    return llm_extraction_strategy

if __name__ == "__main__":
    get_llmextraction_strategy()
