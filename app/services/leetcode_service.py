from typing import Any

from app.clients.leetcode_client import leetcode_client
from app.schemas.graphql_queries import COMPLETE_USER_PROFILE_QUERY
from app.utils.parser import LeetCodeParser
from app.core.exceptions import (
    UserNotFoundError,
    LeetCodeAPIError,
)


class LeetCodeService:
    """
    Service responsible for fetching and parsing
    LeetCode profile data.
    """

    async def get_complete_profile(self, username: str) -> dict[str, Any]:
        """
        Fetch complete LeetCode profile using a
        single GraphQL request.
        """

        try:
         data = await leetcode_client.execute_query(
        COMPLETE_USER_PROFILE_QUERY,
        {
            "username": username
        }
    )

        except UserNotFoundError:
         raise

        except LeetCodeAPIError:
            raise

        except Exception as e:
         raise LeetCodeAPIError(
        f"Failed to fetch data from LeetCode: {str(e)}"
        )

        matched_user = data.get("matchedUser")

        if matched_user is None:
            raise UserNotFoundError(
                f"LeetCode user '{username}' was not found."
            )

        try:
         parsed_profile = LeetCodeParser.parse_complete_profile(data)

        except LeetCodeAPIError:
            raise

        except Exception as e:
           raise LeetCodeAPIError(
            f"Failed to parse LeetCode profile: {str(e)}"
          )
        return parsed_profile


leetcode_service = LeetCodeService()