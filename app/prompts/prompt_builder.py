from typing import Any

from app.prompts.compare_prompt import (
    AI_JUDGE_PROMPT,
    RECRUITER_PROMPT,
    ROAST_PROMPT,
)


class PromptBuilder:

    """
    Builds prompts for the LLM.

    Responsibilities:
    - Select the correct prompt template
    - Convert comparison JSON into readable context
    - Return the final prompt
    """

    @staticmethod
    def build_compare_prompt(
        comparison_data: dict[str, Any],
        mode: str = "ai_judge"
    ) -> str:

        prompt = PromptBuilder.get_prompt_template(mode)

        prompt += "\n\n"

        prompt += PromptBuilder.build_context(
            comparison_data
        )

        return prompt

    @staticmethod
    def get_prompt_template(mode: str) -> str:

        templates = {

            "ai_judge": AI_JUDGE_PROMPT,

            "recruiter": RECRUITER_PROMPT,

            "roast": ROAST_PROMPT

        }

        return templates.get(
            mode.lower(),
            AI_JUDGE_PROMPT
        )

    @staticmethod
    def build_context(
        comparison_data: dict[str, Any]
    ) -> str:

        user1 = comparison_data["user1"]
        user2 = comparison_data["user2"]
        comparison = comparison_data["comparison"]
        winner = comparison_data["winner"]

        context = []

        # ==========================
        # Candidate 1
        # ==========================

        context.append("## Candidate 1")

        context.append(
            f"""
    Username: {user1["username"]}
    Overall Score: {user1["scores"]["overallScore"]}
    Warrior Rank: {user1["scores"]["warriorRank"]}
    Coding Aura: {user1["scores"]["codingAura"]}
    """
        )

        context.append("Strengths:")

        for strength in user1["scores"]["strengths"]:
            context.append(f"- {strength}")

        context.append("\nWeaknesses:")

        for weakness in user1["scores"]["weaknesses"]:
            context.append(f"- {weakness}")

        context.append("\n")

        # ==========================
        # Candidate 2
        # ==========================

        context.append("## Candidate 2")

        context.append(
            f"""
    Username: {user2["username"]}
    Overall Score: {user2["scores"]["overallScore"]}
    Warrior Rank: {user2["scores"]["warriorRank"]}
    Coding Aura: {user2["scores"]["codingAura"]}
    """
        )

        context.append("Strengths:")

        for strength in user2["scores"]["strengths"]:
            context.append(f"- {strength}")

        context.append("\nWeaknesses:")

        for weakness in user2["scores"]["weaknesses"]:
            context.append(f"- {weakness}")

        context.append("\n")

        # ==========================
        # Metric Winners
        # ==========================

        context.append("## Metric Comparison")

        for metric, value in comparison.items():

                context.append(
                    f"- {metric.replace('_', ' ').title()}: "
                    f"{value['winner']} ({value['reason']})"
                )

        return "\n".join(context)

    @staticmethod
    def format_candidate(
        user: dict[str, Any],
        summary: dict[str, Any]
    ) -> str:

        username = user["username"]
        scores = user["scores"]
        info = summary[username]

        text = f"""
    Username: {username}

    Overall Score: {scores['overallScore']}

    Warrior Rank: {scores['warriorRank']}

    Coding Aura: {scores['codingAura']}

    Top Categories:
    """

        for category, score in info["topCategories"]:
            text += f"\n- {category.replace('_', ' ').title()} ({score})"

        text += "\n\nStrengths:"

        for strength in scores["strengths"]:
            text += f"\n- {strength}"

        text += "\n\nWeaknesses:"

        for weakness in scores["weaknesses"]:
            text += f"\n- {weakness}"

        return text


prompt_builder = PromptBuilder()