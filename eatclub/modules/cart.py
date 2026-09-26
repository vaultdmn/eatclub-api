from . import BaseModule
from typing import List, Dict, Optional

class CartModule(BaseModule):
    BASE_URL = "https://cart.box8.co.in"

    def get_cart(self, lat: str, lon: str, outlet_service_type: str = "DEL101", tip_amount: int = 0, cart_items: List[Dict] = None) -> dict:
        """Fetch or update the cart with items."""
        params = {
            "tip_amount": tip_amount,
            "outlet_service_type": outlet_service_type,
            "lat": lat,
            "lon": lon
        }
        payload = {"cart_items": cart_items or []}
        return self._client.request("POST", f"{self.BASE_URL}/cart", params=params, json=payload)

    def update_cart_address(self, lat: str, lon: str, outlet_id: str, address_token: str, outlet_service_type: str = "DEL101") -> dict:
        """Update cart with selected address and outlet."""
        params = {
            "lat": lat,
            "lon": lon
        }
        payload = {
            "outlet_service_type": outlet_service_type,
            "outlet_id": outlet_id,
            "address_token": address_token
        }
        return self._client.request("PUT", f"{self.BASE_URL}/cart", params=params, json=payload)

    def get_offers(self, app_id: str, outlet_id: str, customer_signed_up: str = "false") -> dict:
        """Get applicable offers for the current cart/outlet."""
        params = {
            "app_id": app_id,
            "outlet_id": outlet_id,
            "customer_signed_up": customer_signed_up
        }
        return self._client.request("GET", f"{self.BASE_URL}/v2/offer_details/applicable_offer_details", params=params)

    def validate_order(self, payment_method: str = "cod", **kwargs) -> dict:
        """Validate the order before placement."""
        params = {"payment_method": payment_method}
        params.update(kwargs)
        return self._client.request("GET", f"{self.BASE_URL}/order/validate", params=params)

    def get_credit_balance(self) -> dict:
        """Get customer's EatClub credit balance."""
        return self._client.request("GET", f"{self.BASE_URL}/customer_credit/balance")
