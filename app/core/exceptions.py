"""
Custom exceptions used throughout the application.
"""


class LeetCowarException(Exception):
    """
    Base exception for the application.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class SameUserComparisonError(LeetCowarException):
    """
    Raised when both usernames are identical.
    """
    pass


class UserNotFoundError(LeetCowarException):
    """
    Raised when a LeetCode user does not exist.
    """
    pass


class InvalidUsernameError(LeetCowarException):
    """
    Raised when the username format is invalid.
    """
    pass


class LeetCodeAPIError(LeetCowarException):
    """
    Raised when the LeetCode GraphQL API fails.
    """
    pass


class AIServiceError(LeetCowarException):
    """
    Raised when the AI service fails.
    """
    pass


class PromptBuilderError(LeetCowarException):
    """
    Raised when prompt generation fails.
    """
    pass


class ScoreCalculationError(LeetCowarException):
    """
    Raised when score calculation fails.
    """
    pass


class ComparisonError(LeetCowarException):
    """
    Raised when profile comparison fails.
    """
    pass