# EatClub/Box8 API Python Package Plan

## 1. Overview
The `eatclub_recon` file is a Burp Suite XML export containing HTTP requests and responses from the EatClub (Box8) Android Application. Based on this data, the API consists of several microservices (subdomains) accessed via REST-like JSON endpoints.

The goal is to convert these endpoints into a clean, modular Python package `eatclub` or `eatclub_api`.

## 2. API Architecture Discovered

**Subdomains:**
- `accounts.box8.co.in` - Authentication & Phone verification.
- `api.box8.co.in` - Core API (Customer details, Orders, Core tracking, Addresses).
- `api.box8.in` - Catalog API (Brands, Outlets, Menus/Products).
- `cart.box8.co.in` - Cart & Checkout (Cart management, Offers, Payment methods).
- `customers.box8.co.in` - Customer Profiles.

**Authentication:** 
Token-based via HTTP headers (e.g. `Authorization: Token ...`). Authentication starts with a POST to `/customers/check_phone_status` and `/customers/sign_in`.

**Common Query Parameters:**
Almost all requests require parameters like `platform=android`, `origin=eatclub`, `ver=147`.

## 3. Python Package Structure

```text
eatclub/
├── __init__.py
├── client.py        # Core API client (BaseURL handling, Session, Auth headers)
├── exceptions.py    # Custom exceptions (EatClubAuthError, EatClubAPIError)
├── modules/
│   ├── __init__.py
│   ├── auth.py      # check_phone_status, sign_in
│   ├── catalog.py   # refresh, outlets/apps, outlets/products, banners
│   ├── cart.py      # /cart PUT/POST, applicable_offer_details, validate
│   ├── customer.py  # customer_details, profile, addresses, device
│   └── order.py     # customer_orders, order_tracking_details, active_refunds
```

## 4. Implementation Details

### Core Client (`client.py`)
Will use `httpx` or `requests`. Will maintain a session to persist headers.
```python
class EatClubClient:
    def __init__(self, token=None, version="147"):
        self.session = requests.Session()
        self.version = version
        self.common_params = {
            "platform": "android",
            "origin": "eatclub",
            "ver": self.version
        }
        if token:
            self.set_token(token)
            
        # Initialize modules
        self.auth = AuthModule(self)
        self.catalog = CatalogModule(self)
        ...
```

### Auth Module (`modules/auth.py`)
- `request_otp(phone_no)`: POST `accounts.box8.co.in/customers/check_phone_status` then `sign_in` with `initiate="true"`.
- `verify_otp(phone_no, otp)`: POST `sign_in` with the OTP, retrieve the Auth token, and inject it into the `EatClubClient`.

### Catalog Module (`modules/catalog.py`)
- `get_outlets(lat, lon, brand_id=19)`: GET `api.box8.in/catalog/v4/outlets/apps`.
- `get_products(app_id, outlet_id, service_type)`: POST `api.box8.in/catalog/v2/outlets/products` with `items` in body.

### Cart Module (`modules/cart.py`)
- `add_to_cart(cart_items)`: POST `cart.box8.co.in/cart`.
- `update_cart(outlet_id, address_token, etc)`: PUT `cart.box8.co.in/cart`.
- `get_offers(app_id, outlet_id)`: GET `cart.box8.co.in/v2/offer_details/applicable_offer_details`.

### Customer & Order Modules
- Wrap details fetching, order history (`api.box8.co.in/v3/order/customer_orders`), and tracking endpoints.

## 5. Next Steps
1. Initialize the Python project and `requirements.txt` (e.g., adding `requests`).
2. Write the core `client.py` and `exceptions.py`.
3. Implement the `Auth` module and write a test script to authenticate.
4. Implement `Catalog` module to allow fetching restaurants/menus.
5. Implement `Cart` and `Order` modules to place/track orders.