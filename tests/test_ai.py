import asyncio

from app.prompts.prompt_builder import prompt_builder
from app.services.ai_service import ai_service
from app.services.compare_service import compare_service


async def main():

    comparison = await compare_service.compare_users(
        "samay8193",
        "samay8193"
    )

    prompt = prompt_builder.build_compare_prompt(
        comparison,
        mode="recruiter"
    )

    response = await ai_service.recruiter_mode(
        prompt
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())