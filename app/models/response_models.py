from typing import Any

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    success: bool
    data: dict[str, Any]


class CompareResponse(BaseModel):
    success: bool
    comparison: dict[str, Any]