from fastapi import APIRouter, HTTPException

from app.models.request_models import CompareRequest
from app.services.compare_service import compare_service
from app.core.exceptions import (
    SameUserComparisonError,
    UserNotFoundError,
    LeetCodeAPIError,
    AIServiceError,
    ComparisonError,
)

router = APIRouter(
    prefix="/compare",
    tags=["Compare"]
)


@router.post("")
async def compare_profiles(request: CompareRequest):
    try:

        result = await compare_service.compare_users(
            username1=request.username1,
            username2=request.username2,
            mode=request.mode.value,
        )
        

        return result

    except SameUserComparisonError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except UserNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except (LeetCodeAPIError, AIServiceError) as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except ComparisonError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )