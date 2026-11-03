from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str = Field(description="Short skill name, e.g. 'Python' or 'RAG'")
    category: Literal["technical", "soft", "tool", "domain"]
    evidence: str = Field(description="Exact sentence from the job post that mentions this skill")


class JobRequirements(BaseModel):
    job_title: str
    required_skills: List[Skill]
    nice_to_have: List[Skill]
    years_of_experience: Optional[int] = Field(
        default=None,
        description="Minimum years if stated, otherwise null",
    )


class SkillMatch(BaseModel):
    skill: str
    required: bool
    status: Literal["have", "partial", "missing"]
    candidate_evidence: Optional[str] = Field(
        default=None,
        description="Exact sentence from the candidate profile that shows this skill, or null if missing",
    )


class GapReport(BaseModel):
    matches: List[SkillMatch]
