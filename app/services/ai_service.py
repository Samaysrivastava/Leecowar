import traceback

from google import genai
from google.genai import types

from app.core.config import settings


class AIService:
    """
    AI Service responsible for generating
    comparison analysis using Gemini.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    async def generate_analysis(
        self,
        prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate markdown analysis.
        """

        try:

           

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                ),
            )

           

            # Safely return text
            try:
                if response.text:
                    return response.text
            except Exception as e:
                print("Unable to read response.text")
                print(e)

            # Fallback for debugging
            return str(response)

        except Exception as e:

            print("=" * 80)
            print("GEMINI ERROR")
            traceback.print_exc()
            print("Error:", repr(e))
            print("=" * 80)

            raise RuntimeError(
                f"Gemini Error: {e}"
            )

    async def ai_judge_mode(
        self,
        prompt: str,
    ) -> str:

        return await self.generate_analysis(
            prompt,
            temperature=0.7,
        )

    async def recruiter_mode(
        self,
        prompt: str,
    ) -> str:

        return await self.generate_analysis(
            prompt,
            temperature=0.2,
        )

    async def roast_mode(
        self,
        prompt: str,
    ) -> str:

        return await self.generate_analysis(
            prompt,
            temperature=1.0,
        )


ai_service = AIService()