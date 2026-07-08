import asyncio

from app.clients.leetcode_client import leetcode_client
from app.schemas.graphql_queries import USER_PROFILE_QUERY


async def main():
    data = await leetcode_client.execute_query(
        USER_PROFILE_QUERY,
        {
            "username": "samay8193"
        }
    )

    print(data)


asyncio.run(main())