from . import BaseModule
from typing import List, Dict, Any, Optional

class CatalogModule(BaseModule):
    BASE_URL_API = "https://api.box8.in/catalog"

    def refresh(self, lat: str, lon: str, outlet_id: str, app_id: str = "19", brand_id: str = "19", service_type: str = "DEL101") -> dict:
        """Get the main catalog refresh data (banners, outlet status, memberships)."""
        params = {
            "app_id": app_id,
            "brand_id": brand_id,
            "context": "home",
            "lat": lat,
            "lon": lon,
            "outlet_id": outlet_id,
            "service_type": service_type
        }
        return self._client.request("GET", f"{self.BASE_URL_API}/v1/refresh", params=params)

    def get_outlets(self, lat: str, lon: str, brand_id: str = "19", service_type: str = "DEL101") -> dict:
        """Get nearby outlets for a brand."""
        params = {
            "brand_id": brand_id,
            "lat": lat,
            "lon": lon,
            "service_type": service_type
        }
        return self._client.request("GET", f"{self.BASE_URL_API}/v4/outlets/apps", params=params)

    def get_products(self, outlet_id: str, app_id: str = "19", service_type: str = "DEL101", items: List[Dict] = None) -> dict:
        """Get the product menu for an outlet."""
        params = {
            "app_id": app_id,
            "outlet_id": outlet_id,
            "service_type": service_type
        }
        payload = {"items": items or []}
        return self._client.request("POST", f"{self.BASE_URL_API}/v2/outlets/products", params=params, json=payload)
