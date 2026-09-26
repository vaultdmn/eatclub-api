from . import BaseModule

class OrderModule(BaseModule):
    BASE_URL_API = "https://api.box8.co.in"

    def get_orders(self, page: int = 1, outlet_id: str = None) -> dict:
        """Get order history."""
        params = {"page": page}
        if outlet_id:
            params["outlet_id"] = outlet_id
        return self._client.request("GET", f"{self.BASE_URL_API}/v3/order/customer_orders", params=params)

    def get_tracking_details(self, tracking_id: str, outlet_id: str) -> dict:
        """Track an active order."""
        params = {
            "tracking_id": tracking_id,
            "outlet_id": outlet_id
        }
        return self._client.request("GET", f"{self.BASE_URL_API}/v3/order/order_tracking_details", params=params)

    def get_history_recommendations(self, brand_id: str = "19") -> dict:
        """Get wish-to-repeat recommendations."""
        params = {"brand_id": brand_id}
        return self._client.request("GET", f"{self.BASE_URL_API}/v5/customer/order_history_recommendations", params=params)
