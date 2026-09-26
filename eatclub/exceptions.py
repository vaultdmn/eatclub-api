class EatClubError(Exception):
    """Base exception for EatClub API errors."""
    pass

class EatClubAuthError(EatClubError):
    """Raised when there is an authentication error."""
    pass

class EatClubAPIError(EatClubError):
    """Raised when the API returns an error response."""
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload
