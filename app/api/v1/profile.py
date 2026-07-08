from fastapi import APIRouter, HTTPException

from app.services.leetcode_service import leetcode_service
from app.services.score_service import ScoreService
from app.core.exceptions import (
    UserNotFoundError,
    LeetCodeAPIError,
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/{username}")
async def get_profile(username: str):

    try:

        profile = await leetcode_service.get_complete_profile(
            username
        )

        scores = ScoreService.calculate(profile)

        return {
            "success": True,
            "profile": profile,
            "scores": scores
        }

    except UserNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except LeetCodeAPIError as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )