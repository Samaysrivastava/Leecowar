import asyncio

from app.services.leetcode_service import leetcode_service


async def main():
    data = await leetcode_service.get_complete_profile("samay8193")

    print(data)


asyncio.run(main())