import httpx
from typing import Any, Dict

from app.core.config import settings
from app.core.exceptions import LeetCodeAPIError

class LeetCodeClient:
    """
    Client responsible for communicating with
    LeetCode GraphQL API.
    """

    def __init__(self) -> None:
        self.url = settings.LEETCODE_GRAPHQL

        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        }

        self.timeout = httpx.Timeout(20.0)

    async def execute_query(
    self,
    query: str,
    variables: Dict[str, Any]
) -> Dict[str, Any]:
        """
        Execute any GraphQL query.

        Args:
            query: GraphQL query string.
            variables: Query variables.

        Returns:
            GraphQL data section.
        """

        payload = {
            "query": query,
            "variables": variables,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:

            response = await client.post(
                url=self.url,
                json=payload,
                headers=self.headers,
            )

            response.raise_for_status()

            result = response.json()

            # GraphQL returned errors
            if "errors" in result:

                errors = result["errors"]

                # If every error is "user not found",
                # still return the data so the service layer
                # can raise UserNotFoundError.
                user_not_found = all(
                    "does not exist" in error.get("message", "").lower()
                    for error in errors
                )

                if user_not_found:
                    return result.get("data", {})

                # Any other GraphQL error is an API failure
                raise LeetCodeAPIError(
                    f"GraphQL Error: {errors}"
                )

            return result.get("data", {})


leetcode_client = LeetCodeClient()