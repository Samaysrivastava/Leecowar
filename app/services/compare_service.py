from __future__ import annotations

import asyncio
from typing import Any

from click import prompt

from app.services.leetcode_service import leetcode_service
from app.services.score_service import ScoreService
from app.prompts.prompt_builder import prompt_builder
from app.services.ai_service import ai_service
from app.core.exceptions import SameUserComparisonError


class CompareService:

    """
    Compares two LeetCode users.
    """

    async def compare_users(
        self,
        username1: str,
        username2: str,
        mode: str = "ai_judge",
    ) -> dict[str, Any]:
        if username1.strip().lower() == username2.strip().lower():
             
            raise SameUserComparisonError(
                 "Both usernames are the same. Please enter two different LeetCode usernames."
            )
        
        profile1, profile2 = await asyncio.gather(
            leetcode_service.get_complete_profile(username1),
            leetcode_service.get_complete_profile(username2)
        )

        scores1 = ScoreService.calculate(profile1)
        scores2 = ScoreService.calculate(profile2)

        metric_comparison = self.compare_metrics(
            username1,
            username2,
            scores1,
            scores2
        )

        winner = self.calculate_winner(
            username1,
            username2,
            scores1,
            scores2
        )

        summary = self.generate_summary(
            username1,
            username2,
            scores1,
            scores2
        )

        comparison_data = {

        "user1": {

            "username": username1,

            "profile": profile1,

            "scores": scores1

        },

        "user2": {

            "username": username2,

            "profile": profile2,

            "scores": scores2

        },

        "comparison": metric_comparison,

        "winner": winner,

        "summary": summary

    }
        prompt = prompt_builder.build_compare_prompt(
            comparison_data,
            mode
        )
        # analysis = await ai_service.generate_analysis(
        #     "Compare two students. Student A scored 90, Student B scored 80."
        # )
        if mode == "ai_judge":
            analysis = await ai_service.ai_judge_mode(prompt)

        elif mode == "recruiter":
            analysis = await ai_service.recruiter_mode(prompt)

        elif mode == "roast":
            analysis = await ai_service.roast_mode(prompt)

        else:
            analysis = await ai_service.ai_judge_mode(prompt)
        # comparison_data["analysis"] = "Ai response is currently disabled. Please enable it in the code to get AI analysis."
        comparison_data["analysis"] = analysis
        return comparison_data
    @staticmethod
    def calculate_winner(
        username1: str,
        username2: str,
        scores1: dict[str, Any],
        scores2: dict[str, Any]
    ) -> dict[str, Any]:

        score1 = scores1["overallScore"]
        score2 = scores2["overallScore"]

        if score1 > score2:

            winner = username1

        elif score2 > score1:

            winner = username2

        else:

            winner = "Tie"

        return {

            "winner": winner,

            "score1": score1,

            "score2": score2,

            "difference": abs(score1 - score2)

        }
    @staticmethod
    def compare_metrics(
        username1,
        username2,
        scores1,
        scores2
    ):

        ignored = {

            "overallScore",
            "strengths",
            "weaknesses",
            "grindLevel",
            "codingAura",
            "warriorRank",
            "faangReadiness"

        }

        comparison = {}

        for metric in scores1:

            if metric in ignored:
                continue

            value1 = scores1[metric]
            value2 = scores2[metric]

            if value1 > value2:

                winner = username1

            elif value2 > value1:

                winner = username2

            else:

                winner = "Tie"

            comparison[metric] = {

                "user1": value1,

                "user2": value2,

                "winner": winner,

                "difference": abs(value1 - value2),

                "reason": CompareService.get_metric_reason(
                    metric,
                    value1,
                    value2,
                    winner
                )

            }

        return comparison
    @staticmethod
    def generate_summary(
        username1: str,
        username2: str,
        scores1: dict[str, Any],
        scores2: dict[str, Any]
    ) -> dict[str, Any]:

        metrics = [

            "problemSolving",

            "difficulty",

            "contest",

            "consistency",

            "activity",

            "knowledgeBreadth",

            "advancedTopics",

            "languageDiversity",

            "community",

            "growth",

            "interviewReadiness",

            "competitiveProgramming",

            "momentum"

        ]

        wins1 = 0
        wins2 = 0
        ties = 0

        for metric in metrics:

            if scores1[metric] > scores2[metric]:

                wins1 += 1

            elif scores2[metric] > scores1[metric]:

                wins2 += 1

            else:

                ties += 1

        return {

            username1: {

                "metricsWon": wins1,

                                "topCategories": CompareService.best_categories(
                    scores1
                ),

                "strengths": scores1["strengths"],

                "weaknesses": scores1["weaknesses"],

                "overallScore": scores1["overallScore"],

                "grindLevel": scores1["grindLevel"],

                "warriorRank": scores1["warriorRank"],

                "codingAura": scores1["codingAura"],

                "weaknesses": scores1["weaknesses"]

            },

            username2: {

                "metricsWon": wins2,

                "topCategories": CompareService.best_categories(
    scores2
),

                "strengths": scores2["strengths"],

                "weaknesses": scores2["weaknesses"],

                "overallScore": scores2 ["overallScore"],

                "grindLevel": scores2["grindLevel"],

                "warriorRank": scores2["warriorRank"],

                "codingAura": scores2["codingAura"],

                "weaknesses": scores2["weaknesses"]

            },

            "ties": ties

        }
    @staticmethod
    def get_metric_reason(
        metric: str,
        value1: int,
        value2: int,
        winner: str
    ) -> str:

        difference = abs(value1 - value2)

        if difference == 0:
            return "Both users perform equally in this category."

        reasons = {

            "problemSolving":
                f"{winner} has solved more weighted problems with stronger overall problem-solving performance.",

            "difficulty":
                f"{winner} demonstrates better mastery of Medium and Hard problems.",

            "contest":
                f"{winner} has stronger contest performance based on rating and rankings.",

            "consistency":
                f"{winner} has maintained a more consistent coding streak and activity.",

            "activity":
                f"{winner} has been more active recently on LeetCode.",

            "knowledgeBreadth":
                f"{winner} has solved problems across a wider variety of DSA topics.",

            "advancedTopics":
                f"{winner} shows stronger knowledge in advanced algorithms and data structures.",

            "languageDiversity":
                f"{winner} uses more programming languages while solving problems.",

            "community":
                f"{winner} contributes more to the LeetCode community.",

            "growth":
                f"{winner} has shown better improvement over time.",

            "interviewReadiness":
                f"{winner} appears more prepared for coding interviews.",

            "competitiveProgramming":
                f"{winner} has stronger competitive programming performance.",

            "profileCompleteness":
                f"{winner} has a more complete public profile.",

            "momentum":
                f"{winner} currently has stronger learning momentum."

        }

        return reasons.get(metric, f"{winner} performs better in {metric}.")
    @staticmethod
    def best_categories(scores: dict):

        ignored = {

            "overallScore",

            "strengths",

            "weaknesses",

            "grindLevel",

            "codingAura",

            "warriorRank",

            "faangReadiness"

        }

        metrics = []

        for key, value in scores.items():

            if key in ignored:
                continue

            metrics.append((key, value))

        metrics.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return metrics[:3]

compare_service = CompareService()