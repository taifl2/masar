from langchain_core.output_parsers import PydanticOutputParser

from masar.config import get_llm
from masar.schemas import GapReport, JobRequirements

GAP_PROMPT = """You compare a job's skills with a candidate profile.
For each job skill, decide:
- have: the profile clearly shows this skill
- partial: the profile shows a related or weaker version of it
- missing: the profile does not mention it
Use only what the profile says. Do not assume.
For have or partial, copy the exact sentence from the profile as candidate_evidence.
Return only JSON, with no extra text.

{format_instructions}"""

_parser = PydanticOutputParser(pydantic_object=GapReport)


def analyze_gap(job: JobRequirements, profile_text: str) -> GapReport:
    """Compare the job's skills with the candidate profile."""
    job_skills = "\n".join(
        [f"- {s.name} (required)" for s in job.required_skills]
        + [f"- {s.name} (nice to have)" for s in job.nice_to_have]
    )
    messages = [
        ("system", GAP_PROMPT.format(format_instructions=_parser.get_format_instructions())),
        ("human", f"JOB SKILLS:\n{job_skills}\n\nCANDIDATE PROFILE:\n{profile_text}"),
    ]
    response = get_llm().invoke(messages)
    return _parser.parse(response.content)
