from typing import Any
from app.core.scoring_config import (
    SCORING_CONFIG,
    RANKING_SYSTEM,
)
class ScoreService:

    """
    Calculates deterministic scores for a LeetCode profile.
    All scores are normalized between 0 and 100.
    """

    @staticmethod
    def _clamp(score: float) -> int:
        return max(0, min(100, round(score)))
    @staticmethod
    def get_tier(score: int, tiers: list[tuple[int, str]]) -> str:
        for threshold, name in tiers:
            if score >= threshold:
                return name

        return tiers[-1][1]
    @staticmethod
    def get_rank(score: int, ranking: list[tuple[int, str]]) -> str:

        for threshold, name in ranking:

            if score >= threshold:
                return name

        return ranking[-1][1]
    @staticmethod
    def calculate(profile: dict[str, Any]) -> dict[str, Any]:

        solved = profile["solved"]
        contest = profile["contest"]
        activity = profile["activity"]
        community = profile["community"]
        topics = profile["topics"]
        languages = profile["languages"]
        derived = profile["derived"]

        scores = {}

        scores["problemSolving"] = ScoreService.problem_solving_score(
            solved
        )

        scores["difficulty"] = ScoreService.difficulty_score(
            solved
        )

        scores["contest"] = ScoreService.contest_score(
            contest
        )

        scores["consistency"] = ScoreService.consistency_score(
            activity
        )

        scores["activity"] = ScoreService.activity_score(
            activity
        )

        scores["knowledgeBreadth"] = ScoreService.knowledge_score(
            topics
        )

        scores["advancedTopics"] = ScoreService.advanced_topic_score(
            topics
        )

        scores["languageDiversity"] = ScoreService.language_score(
            languages
        )

        scores["community"] = ScoreService.community_score(
            community
        )

        scores["growth"] = ScoreService.growth_score(
            derived
        )

        scores["profileCompleteness"] = ScoreService.profile_score(
            derived
        )

        scores["interviewReadiness"] = (
            ScoreService.interview_score(
                solved,
                contest,
                topics
            )
        )

        scores["competitiveProgramming"] = (
            ScoreService.cp_score(
                contest
            )
        )

        scores["momentum"] = ScoreService.momentum_score(
            activity
        )

        scores["overallScore"] = (
            ScoreService.overall_score(scores)
        )

        scores["grindLevel"] = (
            ScoreService.grind_level(
                scores["overallScore"]
            )
        )

        scores["codingAura"] = (
            ScoreService.coding_aura(
                scores["overallScore"]
            )
        )

        scores["warriorRank"] = (
            ScoreService.warrior_rank(
                scores["overallScore"]
            )
        )

        scores["faangReadiness"] = (
            ScoreService.faang_readiness(
                scores["overallScore"]
            )
        )
        scores["strengths"] = ScoreService.strengths(scores)

        scores["weaknesses"] = ScoreService.weaknesses(scores)
        return scores
    @staticmethod
    def problem_solving_score(solved: dict[str, Any]) -> int:
        """
        Score based on solved problems.

        Easy   -> 1 point
        Medium -> 2 points
        Hard   -> 4 points

        Normalized to 100.
        """
        config = SCORING_CONFIG["problem_solving"]
        weighted = (
              solved["easy"] * config["easy_weight"]
            + solved["medium"] * config["medium_weight"]
            + solved["hard"] * config["hard_weight"]
        )

        score = (
        weighted /
        config["normalization_factor"]
        ) * 100

        return ScoreService._clamp(score)

    @staticmethod
    def difficulty_score(solved: dict[str, Any]) -> int:
        """
        Reward users who solve harder problems.
        """

        total = solved["total"]

        if total == 0:
            return 0

        weighted = (
            solved["easy"] * 1
            + solved["medium"] * 3
            + solved["hard"] * 6
        )

        max_possible = total * 6

        score = (weighted / max_possible) * 100

        return ScoreService._clamp(score)

    @staticmethod
    def contest_score(contest: dict[str, Any]) -> int:
        """
        Based on contest rating,
        participation and ranking.
        """

        rating = contest.get("rating", 0) or 0
        attended = contest.get("attended", 0)
        top = contest.get("topPercentage", 100)

        rating_score = min((rating / 2500) * 60, 60)

        participation_score = min(attended * 0.8, 20)

        ranking_score = max(0, 20 - (top / 5))

        return ScoreService._clamp(
            rating_score
            + participation_score
            + ranking_score
        )

    @staticmethod
    def consistency_score(activity: dict[str, Any]) -> int:
        """
        Based on streak and active days.
        """

        streak = activity.get("streak", 0)
        active_days = activity.get(
            "totalActiveDays",
            0
        )

        streak_score = min(streak, 40)

        active_score = min(
            active_days / 5,
            60
        )

        return ScoreService._clamp(
            streak_score + active_score
        )

    @staticmethod
    def activity_score(activity: dict[str, Any]) -> int:
        """
        Recent activity score.
        """

        submissions = activity.get(
            "recentSubmissionCount",
            0
        )

        active_days = activity.get(
            "totalActiveDays",
            0
        )

        score = (
            min(submissions * 4, 40)
            +
            min(active_days / 4, 60)
        )

        return ScoreService._clamp(score)
    @staticmethod
    def knowledge_score(topics: dict[str, Any]) -> int:
        """
        Measures topic coverage.
        More unique topics solved = higher score.
        """

        total_topics = topics.get("totalTopics", 0)

        score = (total_topics / 60) * 100

        return ScoreService._clamp(score)

    @staticmethod
    def advanced_topic_score(topics: dict[str, Any]) -> int:
        """
        Rewards solving advanced topics like
        DP, Graph, Trie, Segment Tree, etc.
        """

        advanced = topics.get("advanced", [])

        solved = sum(
            topic.get("problemsSolved", 0)
            for topic in advanced
        )

        score = (solved / 250) * 100

        return ScoreService._clamp(score)

    @staticmethod
    def language_score(languages: dict[str, Any]) -> int:
        """
        Rewards solving problems in multiple languages.
        """

        count = languages.get("count", 0)

        score = min(count * 20, 100)

        return ScoreService._clamp(score)

    @staticmethod
    def community_score(community: dict[str, Any]) -> int:
        """
        Measures community contribution.
        """

        badges = community.get("badgeCount", 0)

        solutions = community.get(
            "solutionCount",
            0
        )

        discussions = community.get(
            "discussionCount",
            0
        )

        views = community.get(
            "postViews",
            0
        )

        score = (
            badges * 10
            +
            solutions * 2
            +
            discussions * 1.5
            +
            (views / 100)
        )

        return ScoreService._clamp(score)

    @staticmethod
    def growth_score(
        derived: dict[str, Any]
    ) -> int:
        """
        Uses contest improvement.
        """

        growth = derived.get(
            "contestGrowth",
            0
        )

        score = 50 + (growth / 20)

        return ScoreService._clamp(score)

    @staticmethod
    def profile_score(
        derived: dict[str, Any]
    ) -> int:
        """
        Rewards complete public profiles.
        """

        return ScoreService._clamp(
            derived.get(
                "profileCompleteness",
                0
            )
        )
    
    @staticmethod
    def interview_score(
        solved: dict[str, Any],
        contest: dict[str, Any],
        topics: dict[str, Any]
    ) -> int:
        """
        Estimates interview readiness based on:
        - Medium problems
        - Hard problems
        - Contest rating
        - Topic coverage
        """

        medium_score = min(
            (solved.get("medium", 0) / 400) * 40,
            40
        )

        hard_score = min(
            (solved.get("hard", 0) / 150) * 30,
            30
        )

        contest_score = min(
            ((contest.get("rating", 0) or 0) / 2200) * 20,
            20
        )

        topic_score = min(
            (topics.get("totalTopics", 0) / 60) * 10,
            10
        )

        return ScoreService._clamp(
            medium_score +
            hard_score +
            contest_score +
            topic_score
        )

    @staticmethod
    def cp_score(
        contest: dict[str, Any]
    ) -> int:
        """
        Competitive Programming Score.
        """

        rating = contest.get(
            "rating",
            0
        ) or 0

        contests = contest.get(
            "attended",
            0
        )

        top = contest.get(
            "topPercentage",
            100
        )

        rating_score = min(
            (rating / 2500) * 70,
            70
        )

        participation_score = min(
            contests * 0.5,
            15
        )

        ranking_score = max(
            0,
            15 - (top / 7)
        )

        return ScoreService._clamp(
            rating_score +
            participation_score +
            ranking_score
        )

    @staticmethod
    def momentum_score(
        activity: dict[str, Any]
    ) -> int:
        """
        Measures recent activity momentum.
        """

        streak = activity.get(
            "streak",
            0
        )

        submissions = activity.get(
            "recentSubmissionCount",
            0
        )

        score = (
            min(streak * 2, 60)
            +
            min(submissions * 2, 40)
        )

        return ScoreService._clamp(score)

    @staticmethod
    def overall_score(
        scores: dict[str, Any]
    ) -> int:
        """
        Weighted overall score.
        """

        weights = SCORING_CONFIG["overall_weights"]

        total = 0

        for metric, weight in weights.items():
            total += scores[metric] * weight

        return ScoreService._clamp(total)
    
    @staticmethod
    def grind_level(overall_score: int) -> str:
        """
        Represents how much effort a user has put into LeetCode.
        """

        if overall_score >= 95:
            return "S+"

        if overall_score >= 90:
            return "S"

        if overall_score >= 80:
            return "A+"

        if overall_score >= 70:
            return "A"

        if overall_score >= 60:
            return "B"

        if overall_score >= 50:
            return "C"

        return "Beginner"

    @staticmethod
    def coding_aura(score: int) -> str:

        return ScoreService.get_tier(
            score,
            RANKING_SYSTEM["coding_aura"]
        )

    @staticmethod
    def warrior_rank(score: int) -> str:

        return ScoreService.get_tier(
        score,
        RANKING_SYSTEM["warrior_rank"]
        )

    @staticmethod
    def faang_readiness(score: int) -> str:

        return ScoreService.get_tier(
            score,
            RANKING_SYSTEM["faang"]
        )
    @staticmethod
    def strengths(scores: dict[str, Any]) -> list[str]:

        strengths = []

        if scores["problemSolving"] >= 80:
            strengths.append(
                "Excellent problem solving ability."
            )

        if scores["difficulty"] >= 80:
            strengths.append(
                "Strong at solving difficult problems."
            )

        if scores["contest"] >= 75:
            strengths.append(
                "Strong contest performance."
            )

        if scores["knowledgeBreadth"] >= 75:
            strengths.append(
                "Good coverage of different DSA topics."
            )

        if scores["consistency"] >= 75:
            strengths.append(
                "Consistent coding practice."
            )

        if scores["interviewReadiness"] >= 80:
            strengths.append(
                "Well prepared for technical interviews."
            )

        if not strengths:
            strengths.append(
                "Shows steady learning progress."
            )

        return strengths

    @staticmethod
    def weaknesses(scores: dict[str, Any]) -> list[str]:

        weaknesses = []

        if scores["difficulty"] < 60:
            weaknesses.append(
                "Solve more Medium and Hard problems."
            )

        if scores["contest"] < 60:
            weaknesses.append(
                "Participate in more weekly contests."
            )

        if scores["knowledgeBreadth"] < 60:
            weaknesses.append(
                "Practice a wider range of DSA topics."
            )

        if scores["community"] < 40:
            weaknesses.append(
                "Contribute more solutions and discussions."
            )

        if scores["languageDiversity"] < 40:
            weaknesses.append(
                "Explore solving problems in multiple languages."
            )

        if scores["consistency"] < 60:
            weaknesses.append(
                "Maintain a longer daily solving streak."
            )

        if not weaknesses:
            weaknesses.append(
                "No major weaknesses identified."
            )

        return weaknesses