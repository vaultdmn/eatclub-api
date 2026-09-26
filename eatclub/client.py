import requests
from typing import Optional, Dict, Any

from .exceptions import EatClubAPIError, EatClubAuthError
from .modules.auth import AuthModule
from .modules.catalog import CatalogModule
from .modules.cart import CartModule
from .modules.customer import CustomerModule
from .modules.order import OrderModule

class EatClubClient:
    def __init__(self, token: Optional[str] = None, version: str = "147"):
        self.session = requests.Session()
        self.version = version

        # Default query parameters added to every request
        self.default_params = {
            "platform": "android",
            "origin": "eatclub",
            "ver": self.version
        }

        self.session.headers.update({
            "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android 11; sdk_gphone_x86 Build/RSR1.201013.001)",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
        })

        if token:
            self.set_token(token)

        # Initialize API modules
        self.auth = AuthModule(self)
        self.catalog = CatalogModule(self)
        self.cart = CartModule(self)
        self.customer = CustomerModule(self)
        self.order = OrderModule(self)

    def set_token(self, token: str):
        """Set the authentication token for the session."""
        self.session.headers.update({
            "Authorization": f"Token {token}"
        })

    def request(self, method: str, url: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Base request method that handles default params and error raising."""
        # Merge default params with request-specific params
        req_params = self.default_params.copy()
        if params:
            req_params.update(params)

        response = self.session.request(method, url, params=req_params, **kwargs)

        try:
            data = response.json()
        except ValueError:
            raise EatClubAPIError(f"Invalid JSON response: {response.text}", status_code=response.status_code)

        if not response.ok:
            if response.status_code == 401:
                raise EatClubAuthError("Unauthorized. Token may be invalid or expired.")
            raise EatClubAPIError(
                message=data.get("message") or data.get("error") or "API Request Failed",
                status_code=response.status_code,
                payload=data
            )

        return data
