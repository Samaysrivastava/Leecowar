"""
All GraphQL queries used by the backend.

These queries are centralized here so that
if LeetCode changes its GraphQL schema,
only this file needs to be updated.
"""

# ==========================================================
# COMPLETE USER PROFILE
# ==========================================================

COMPLETE_USER_PROFILE_QUERY = """
query getCompleteUserProfile($username: String!) {

  matchedUser(username: $username) {

    username

    profile {
      realName
      userAvatar
      reputation
      ranking
      starRating
      aboutMe
      countryName
      company
      school

      skillTags

      postViewCount
      postViewCountDiff

      solutionCount
      categoryDiscussCount

      certificationLevel
    }

    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }

    badges {
      id
      displayName
      icon
      creationDate
    }

    languageProblemCount {
      languageName
      problemsSolved
    }

    tagProblemCounts {

      advanced {
        tagName
        problemsSolved
      }

      intermediate {
        tagName
        problemsSolved
      }

      fundamental {
        tagName
        problemsSolved
      }
    }

    userCalendar {
      activeYears
      streak
      totalActiveDays
      submissionCalendar
    }
  }

  userContestRanking(username: $username) {

      attendedContestsCount

      rating

      globalRanking

      totalParticipants

      topPercentage

      badge {
          name
      }
  }

  userContestRankingHistory(username: $username) {

      attended

      trendDirection

      problemsSolved

      totalProblems

      finishTimeInSeconds

      rating

      ranking

      contest {
          title
          startTime
      }
  }

  recentSubmissionList(username: $username) {

      title

      titleSlug

      statusDisplay

      lang

      timestamp
  }

}
"""