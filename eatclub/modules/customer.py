from . import BaseModule

class CustomerModule(BaseModule):
    BASE_URL_API = "https://api.box8.co.in"
    BASE_URL_CUSTOMERS = "https://customers.box8.co.in"

    def get_details(self, customer_token: str = None) -> dict:
        """Get customer details. POST request with token (sometimes optional if header present)."""
        payload = {}
        if customer_token:
            payload["customer_token"] = customer_token
        return self._client.request("POST", f"{self.BASE_URL_API}/v3/customer/customer_details", json=payload)

    def get_profile(self) -> dict:
        """Get customer profile."""
        return self._client.request("GET", f"{self.BASE_URL_CUSTOMERS}/customer/profile")

    def get_addresses(self, outlet_id: str = None) -> dict:
        """Get saved customer addresses."""
        params = {}
        if outlet_id:
            params["outlet_id"] = outlet_id
        return self._client.request("GET", f"{self.BASE_URL_API}/v2/customer_address", params=params)

    def get_bottom_strip_details(self) -> dict:
        """Get bottom strip details (used in app UI, sometimes has useful status info)."""
        return self._client.request("GET", f"{self.BASE_URL_API}/v5/customer/bottom_strip_details")
