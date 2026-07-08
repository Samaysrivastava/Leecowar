"""
Centralized scoring configuration.

Every scoring function reads values from here.
Changing this file changes the entire ranking algorithm.
"""

SCORING_CONFIG = {

    # --------------------------------------------------
    # Problem Solving
    # --------------------------------------------------
    "problem_solving": {

        "easy_weight": 1,

        "medium_weight": 3,

        "hard_weight": 6,

        "normalization_factor": 3000

    },

    # --------------------------------------------------
    # Difficulty
    # --------------------------------------------------

    "difficulty": {

        "easy_weight": 1,

        "medium_weight": 3,

        "hard_weight": 6

    },

    # --------------------------------------------------
    # Contest
    # --------------------------------------------------

    "contest": {

        "max_rating": 2500,

        "rating_weight": 60,

        "participation_weight": 20,

        "ranking_weight": 20,

        "max_participation": 25

    },

    # --------------------------------------------------
    # Consistency
    # --------------------------------------------------

    "consistency": {

        "max_streak": 40,

        "max_active_days": 300

    },

    # --------------------------------------------------
    # Activity
    # --------------------------------------------------

    "activity": {

        "submission_weight": 4,

        "max_recent_submission_score": 40,

        "max_active_score": 60

    },

    # --------------------------------------------------
    # Topics
    # --------------------------------------------------

    "topics": {

        "expected_total_topics": 60,

        "expected_advanced_problems": 250

    },

    # --------------------------------------------------
    # Languages
    # --------------------------------------------------

    "languages": {

        "score_per_language": 20,

        "max_score": 100

    },

    # --------------------------------------------------
    # Community
    # --------------------------------------------------

    "community": {

        "badge_weight": 10,

        "solution_weight": 2,

        "discussion_weight": 1.5,

        "view_divisor": 100

    },

    # --------------------------------------------------
    # Growth
    # --------------------------------------------------

    "growth": {

        "base_score": 50,

        "growth_divisor": 20

    },

    # --------------------------------------------------
    # Interview Readiness
    # --------------------------------------------------

    "interview": {

        "max_medium": 400,

        "max_hard": 150,

        "max_rating": 2200,

        "max_topics": 60

    },

    # --------------------------------------------------
    # Competitive Programming
    # --------------------------------------------------

    "cp": {

        "max_rating": 2500,

        "max_contests": 30

    },

    # --------------------------------------------------
    # Momentum
    # --------------------------------------------------

    "momentum": {

        "streak_multiplier": 2,

        "submission_multiplier": 2

    },

    # --------------------------------------------------
    # Overall Score Weights
    # --------------------------------------------------

    "overall_weights": {

        "problemSolving": 0.20,

        "difficulty": 0.15,

        "contest": 0.15,

        "consistency": 0.10,

        "activity": 0.05,

        "knowledgeBreadth": 0.10,

        "advancedTopics": 0.05,

        "languageDiversity": 0.02,

        "community": 0.03,

        "growth": 0.05,

        "profileCompleteness": 0.02,

        "interviewReadiness": 0.05,

        "competitiveProgramming": 0.02,

        "momentum": 0.01

    }
}

RANKING_SYSTEM = {

    "warrior_rank": [

        (95, "Grandmaster"),

        (90, "Master"),

        (80, "Diamond"),

        (70, "Platinum"),

        (60, "Gold"),

        (50, "Silver"),

        (0, "Bronze")

    ],

    "coding_aura": [

        (95, "Legendary"),

        (90, "Elite"),

        (80, "Excellent"),

        (70, "Strong"),

        (60, "Promising"),

        (50, "Learning"),

        (0, "Rookie")

    ],

    "faang": [

        (95, "FAANG Ready"),

        (85, "Highly Competitive"),

        (75, "Interview Ready"),

        (65, "Needs More Practice"),

        (50, "Learning Phase"),

        (0, "Beginner")

    ]
}