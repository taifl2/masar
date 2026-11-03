from langchain_core.output_parsers import PydanticOutputParser

from masar.config import get_llm
from masar.schemas import JobRequirements

SYSTEM_PROMPT = """You analyze job postings.
Extract only what the posting actually says. Do not guess or add skills.
For every skill, copy the exact sentence from the posting as evidence.
Put skills marked as 'preferred', 'plus' or 'nice to have' in nice_to_have.
Return only JSON, with no extra text.

{format_instructions}"""

_parser = PydanticOutputParser(pydantic_object=JobRequirements)


def analyze_job(job_text: str) -> JobRequirements:
    """Extract the required and nice-to-have skills from a job posting."""
    messages = [
        ("system", SYSTEM_PROMPT.format(format_instructions=_parser.get_format_instructions())),
        ("human", job_text),
    ]
    response = get_llm().invoke(messages)
    return _parser.parse(response.content)
