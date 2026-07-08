from enum import Enum

from pydantic import BaseModel, Field


class ComparisonMode(str, Enum):
    ai_judge = "ai_judge"
    recruiter = "recruiter"
    roast = "roast"


class CompareRequest(BaseModel):
    username1: str = Field(
        ...,
        min_length=1,
        description="First LeetCode username"
    )

    username2: str = Field(
        ...,
        min_length=1,
        description="Second LeetCode username"
    )

    mode: ComparisonMode = Field(
        default=ComparisonMode.ai_judge,
        description="Comparison mode"
    )