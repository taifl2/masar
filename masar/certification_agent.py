from langchain_core.output_parsers import PydanticOutputParser

from masar.config import get_llm
from masar.knowledge_base import get_index
from masar.schemas import CertPlan, GapReport, JobRequirements

MIN_SCORE = 0.30

CERT_PROMPT = """You recommend professional certifications.
You get the candidate's missing skills and a list of certifications.
Pick at most 3 certifications that best cover the missing skills.
Use only certifications from the list, with their exact id.
If no certification fits a skill, leave that skill uncovered. Do not invent certifications.
In the reason, mention only skills that appear in that certification's skills list.
Return only JSON, with no extra text.

{format_instructions}"""

_parser = PydanticOutputParser(pydantic_object=CertPlan)


def find_candidates(queries: list[str], k: int = 3) -> dict:
    """Search the knowledge base and keep only results above MIN_SCORE."""
    index = get_index()
    candidates = {}
    for query in queries:
        for cert, score in index.search(query, k=k):
            if score >= MIN_SCORE:
                candidates[cert["id"]] = cert
    return candidates


def recommend_certs(job: JobRequirements, gap: GapReport) -> CertPlan:
    """Recommend certifications from the knowledge base for the missing skills."""
    evidence = {s.name: s.evidence for s in job.required_skills + job.nice_to_have}
    missing = [m.skill for m in gap.matches if m.status != "have"]
    # Search with the skill plus its sentence from the job post, not the bare name
    queries = [f"{s}. {evidence.get(s, '')}" for s in missing]
    candidates = find_candidates(queries)
    if not candidates:
        return CertPlan(recommendations=[])

    missing_list = "\n".join(f"- {s}" for s in missing)
    cert_list = "\n".join(
        f"- id: {c['id']} | {c['name']} ({c['issuer']}) | skills: {', '.join(c['skills'])}"
        for c in candidates.values()
    )
    messages = [
        ("system", CERT_PROMPT.format(format_instructions=_parser.get_format_instructions())),
        ("human", f"MISSING SKILLS:\n{missing_list}\n\nCERTIFICATIONS:\n{cert_list}"),
    ]
    plan = _parser.parse(get_llm().invoke(messages).content)

    # Guardrail: drop any certification that was not retrieved
    plan.recommendations = [r for r in plan.recommendations if r.cert_id in candidates]
    return plan
