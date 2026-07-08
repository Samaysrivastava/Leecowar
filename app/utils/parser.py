from typing import Any


class LeetCodeParser:
    """
    Converts raw LeetCode GraphQL response
    into a normalized profile for the Score Engine
    and AI comparison.
    """

    @staticmethod
    def parse_complete_profile(data: dict[str, Any]) -> dict[str, Any]:

        matched_user = data.get("matchedUser")

        if matched_user is None:
            return {}

        return {

            "username": matched_user.get("username"),

            "basic": LeetCodeParser._parse_basic(
                matched_user
            ),

            "solved": LeetCodeParser._parse_solved(
                matched_user
            ),

            "contest": LeetCodeParser._parse_contest(
                data
            ),

            "activity": LeetCodeParser._parse_activity(
                matched_user,
                data
            ),

            "community": LeetCodeParser._parse_community(
                matched_user
            ),

            "topics": LeetCodeParser._parse_topics(
                matched_user
            ),

            "languages": LeetCodeParser._parse_languages(
                matched_user
            ),

            "derived": LeetCodeParser._calculate_derived_metrics(
                matched_user,
                data
            )
        }
    @staticmethod
    def _parse_basic(user: dict[str, Any]) -> dict[str, Any]:

        profile = user.get("profile") or {}

        return {

            "name": profile.get("realName"),

            "avatar": profile.get("userAvatar"),

            "country": profile.get("countryName"),

            "company": profile.get("company"),

            "school": profile.get("school"),

            "about": profile.get("aboutMe"),

            "ranking": profile.get("ranking"),

            "reputation": profile.get("reputation"),

            "starRating": profile.get("starRating"),

            "certificationLevel": profile.get(
                "certificationLevel"
            ),

            "skillTags": profile.get(
                "skillTags",
                []
            )
        }
    @staticmethod
    def _parse_solved(user: dict[str, Any]) -> dict[str, Any]:

        solved = {}

        for item in user.get(
            "submitStats",
            {}
        ).get(
            "acSubmissionNum",
            []
        ):

            solved[item["difficulty"]] = {

                "count": item["count"],

                "submissions": item["submissions"]
            }

        return {

            "total": solved.get(
                "All",
                {}
            ).get(
                "count",
                0
            ),

            "easy": solved.get(
                "Easy",
                {}
            ).get(
                "count",
                0
            ),

            "medium": solved.get(
                "Medium",
                {}
            ).get(
                "count",
                0
            ),

            "hard": solved.get(
                "Hard",
                {}
            ).get(
                "count",
                0
            ),

            "acceptedSubmissions": solved.get(
                "All",
                {}
            ).get(
                "submissions",
                0
            )
        }
    @staticmethod
    def _parse_contest(
        data: dict[str, Any]
    ) -> dict[str, Any]:

        contest = data.get(
            "userContestRanking"
        ) or {}

        history = data.get(
            "userContestRankingHistory"
        ) or []

        return {

            "rating": contest.get(
                "rating",
                0
            ),

            "globalRanking": contest.get(
                "globalRanking",
                0
            ),

            "topPercentage": contest.get(
                "topPercentage",
                100
            ),

            "attended": contest.get(
                "attendedContestsCount",
                0
            ),

            "totalParticipants": contest.get(
                "totalParticipants",
                0
            ),

            "badge": contest.get(
                "badge"
            ),

            "history": history
        }
    @staticmethod
    def _parse_activity(
        user: dict[str, Any],
        data: dict[str, Any]
    ) -> dict[str, Any]:

        calendar = user.get("userCalendar") or {}

        recent_submissions = data.get(
            "recentSubmissionList"
            
        ) or []

        return {

            "streak": calendar.get(
                "streak",
                0
            ),

            "activeYears": calendar.get(
                "activeYears",
                []
            ),

            "totalActiveDays": calendar.get(
                "totalActiveDays",
                0
            ),

            "submissionCalendar": calendar.get(
                "submissionCalendar",
                "{}"
            ),

            "recentSubmissions": recent_submissions,

            "recentSubmissionCount": len(
                recent_submissions
            )
        }
    @staticmethod
    def _parse_community(
        user: dict[str, Any]
    ) -> dict[str, Any]:

        profile = user.get("profile") or {}

        badges = user.get(
            "badges",
            []
        )

        badge_names = [
            badge.get("displayName")
            for badge in badges
        ]

        return {

            "badgeCount": len(
                badges
            ),

            "badges": badge_names,

            "solutionCount": profile.get(
                "solutionCount",
                0
            ),

            "discussionCount": profile.get(
                "categoryDiscussCount",
                0
            ),

            "postViews": profile.get(
                "postViewCount",
                0
            ),

            "postViewGrowth": profile.get(
                "postViewCountDiff",
                0
            ),

            "reputation": profile.get(
                "reputation",
                0
            )
        }
    @staticmethod
    def _parse_topics(
        user: dict[str, Any]
    ) -> dict[str, Any]:

        topic_counts = user.get(
            "tagProblemCounts"
        ) or {}

        fundamental = topic_counts.get(
            "fundamental",
            []
        )

        intermediate = topic_counts.get(
            "intermediate",
            []
        )

        advanced = topic_counts.get(
            "advanced",
            []
        )

        return {

            "fundamental": fundamental,

            "intermediate": intermediate,

            "advanced": advanced,

            "fundamentalCount": len(
                fundamental
            ),

            "intermediateCount": len(
                intermediate
            ),

            "advancedCount": len(
                advanced
            ),

            "totalTopics": (
                len(fundamental)
                + len(intermediate)
                + len(advanced)
            )
        }
    @staticmethod
    def _parse_languages(
        user: dict[str, Any]
    ) -> dict[str, Any]:

        languages = user.get(
            "languageProblemCount"
        ) or []

        parsed_languages = []

        total_problems = 0

        for language in languages:

            parsed_languages.append({

                "name": language.get(
                    "languageName"
                ),

                "solved": language.get(
                    "problemsSolved",
                    0
                )
            })

            total_problems += language.get(
                "problemsSolved",
                0
            )

        parsed_languages.sort(
            key=lambda x: x["solved"],
            reverse=True
        )

        return {

            "count": len(
                parsed_languages
            ),

            "totalSolvedAcrossLanguages": total_problems,

            "primaryLanguage": (
                parsed_languages[0]["name"]
                if parsed_languages
                else None
            ),

            "languages": parsed_languages
        }
    @staticmethod
    def _calculate_derived_metrics(
        user: dict[str, Any],
        data: dict[str, Any]
    ) -> dict[str, Any]:

        # -------------------------------
        # Solved Statistics
        # -------------------------------

        submit_stats = user.get(
            "submitStats",
            {}
        ).get(
            "acSubmissionNum",
            []
        )

        solved = {}

        for item in submit_stats:
            solved[item["difficulty"]] = item["count"]

        total = solved.get("All", 0)
        easy = solved.get("Easy", 0)
        medium = solved.get("Medium", 0)
        hard = solved.get("Hard", 0)

        # -------------------------------
        # Contest Statistics
        # -------------------------------

        contest = data.get(
            "userContestRanking"
        ) or {}

        contest_history = data.get(
            "userContestRankingHistory"
            
        ) or []

        contest_count = contest.get(
            "attendedContestsCount",
            0
        )

        rating = contest.get(
            "rating",
            0
        ) or 0

        # -------------------------------
        # Community
        # -------------------------------

        badges = user.get("badges") or []

        profile = user.get("profile") or {}

        # -------------------------------
        # Topics
        # -------------------------------

        topic_counts = user.get(
            "tagProblemCounts"
        ) or {}

        total_topics = (
            len(topic_counts.get("fundamental", []))
            + len(topic_counts.get("intermediate", []))
            + len(topic_counts.get("advanced", []))
        )

        # -------------------------------
        # Languages
        # -------------------------------

        language_count = user.get(
            "languageProblemCount"
        ) or []

        # -------------------------------
        # Calendar
        # -------------------------------

        calendar = user.get(
            "userCalendar"
        ) or {}

        streak = calendar.get(
            "streak",
            0
        )

        active_days = calendar.get(
            "totalActiveDays",
            0
        )

        # -------------------------------
        # Ratios
        # -------------------------------

        hard_ratio = (
            round((hard / total) * 100, 2)
            if total else 0
        )

        medium_ratio = (
            round((medium / total) * 100, 2)
            if total else 0
        )

        easy_ratio = (
            round((easy / total) * 100, 2)
            if total else 0
        )

        # -------------------------------
        # Profile Completeness
        # -------------------------------

        completeness = 0

        fields = [
            profile.get("realName"),
            profile.get("userAvatar"),
            profile.get("countryName"),
            profile.get("company"),
            profile.get("school"),
            profile.get("aboutMe"),
        ]

        for field in fields:
            if field:
                completeness += 1

        profile_completeness = round(
            (completeness / len(fields)) * 100,
            2
        )

        # -------------------------------
        # Growth
        # -------------------------------

        contest_growth = 0

        ratings = [
            h.get("rating")
            for h in contest_history
            if h.get("rating")
        ]

        if len(ratings) >= 2:
            contest_growth = ratings[-1] - ratings[0]

        # -------------------------------
        # Experience Level
        # -------------------------------

        if total >= 2000:
            experience = "Elite"

        elif total >= 1000:
            experience = "Expert"

        elif total >= 500:
            experience = "Advanced"

        elif total >= 200:
            experience = "Intermediate"

        else:
            experience = "Beginner"

        # -------------------------------
        # Return
        # -------------------------------

        return {

            "easyRatio": easy_ratio,

            "mediumRatio": medium_ratio,

            "hardRatio": hard_ratio,

            "badgeCount": len(
                badges
            ),

            "topicCount": total_topics,

            "languageCount": language_count,

            "contestCount": contest_count,

            "contestRating": rating,

            "contestGrowth": contest_growth,

            "activeDays": active_days,

            "streak": streak,

            "profileCompleteness": profile_completeness,

            "experienceLevel": experience,

            "solutionCount": profile.get(
                "solutionCount",
                0
            ),

            "discussionCount": profile.get(
                "categoryDiscussCount",
                0
            ),

            "postViews": profile.get(
                "postViewCount",
                0
            ),

            "reputation": profile.get(
                "reputation",
                0
            )
        }