class BaseModule:
    """Base class for all EatClub API modules."""
    def __init__(self, client):
        self._client = client
