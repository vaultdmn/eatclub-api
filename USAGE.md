# Detailed Usage Guide for EatClub API

This document provides in-depth technical details on the various methods available in the `eatclub` package, along with code snippets and payload descriptions.

---

## Table of Contents
1. [Initialization](#initialization)
2. [Auth Module](#auth-module)
3. [Catalog Module](#catalog-module)
4. [Cart Module](#cart-module)
5. [Customer Module](#customer-module)
6. [Order Module](#order-module)
7. [Exceptions](#exceptions)

---

## 1. Initialization

Initialize the `EatClubClient` instance:

```python
from eatclub import EatClubClient

# Standard initialization
client = EatClubClient()

# Initialize with a pre-existing token
client = EatClubClient(token="YOUR_AUTH_TOKEN")

# Custom App version override (defaults to "147")
client = EatClubClient(version="148")
```

---

## 2. Auth Module

Manages phone OTP validation and token acquisition.

### `request_otp(phone_no: str) -> dict`
Initiates an OTP request to the specified Indian phone number.
```python
response = client.auth.request_otp("9876543210")
# Returns metadata about OTP status
```

### `verify_otp(phone_no: str, otp: str, set_token: bool = True) -> dict`
Validates the OTP sent to your phone. If `set_token=True`, the acquired session token is automatically attached to `client`.
```python
auth_data = client.auth.verify_otp("9876543210", "1234")
```

---

## 3. Catalog Module

Access brands, available products, and outlets.

### `get_outlets(lat: str, lon: str, brand_id: str = "19", service_type: str = "DEL101") -> dict`
Find outlets that deliver to the specified coordinates.
```python
outlets = client.catalog.get_outlets(lat="28.513188", lon="77.077349")
```

### `get_products(outlet_id: str, app_id: str = "19", service_type: str = "DEL101", items: list = None) -> dict`
Fetch menus, products, pricing, and category breakdowns.
```python
menu = client.catalog.get_products(outlet_id="353")
```

### `refresh(lat: str, lon: str, outlet_id: str, ...) -> dict`
Performs a main refresh of the dashboard/banners for the current outlet.

---

## 4. Cart Module

Build a cart, apply promos, and check balances.

### `get_cart(lat: str, lon: str, outlet_service_type: str = "DEL101", tip_amount: int = 0, cart_items: list = None) -> dict`
Calculates subtotal, discounts, delivery fees, and updates cart contents.
```python
cart = client.cart.get_cart(
    lat="28.513188",
    lon="77.077349",
    cart_items=[
        {"item_id": "1234", "quantity": 2}
    ]
)
```

### `get_credit_balance() -> dict`
Returns your wallet or credit balance.
```python
balance = client.cart.get_credit_balance()
print(balance)
```

### `get_offers(app_id: str, outlet_id: str, customer_signed_up: str = "false") -> dict`
Retrieves applicable coupons, passes, and promotional deals.
```python
offers = client.cart.get_offers(app_id="19", outlet_id="353")
```

---

## 5. Customer Module

Manage the user's account details and delivery addresses.

### `get_profile() -> dict`
Returns the user's profile info.
```python
profile = client.customer.get_profile()
```

### `get_addresses(outlet_id: str = None) -> dict`
Returns all saved addresses for the customer.
```python
addresses = client.customer.get_addresses()
```

---

## 6. Order Module

Track and fetch history of past orders.

### `get_orders(page: int = 1, outlet_id: str = None) -> dict`
Retrieve a paginated list of previous orders.
```python
orders = client.order.get_orders(page=1)
```

### `get_tracking_details(tracking_id: str, outlet_id: str) -> dict`
Get live GPS and delivery status for an active order.
```python
tracking = client.order.get_tracking_details(tracking_id="TRK12345", outlet_id="353")
```

---

## 7. Exceptions

All custom exceptions inherit from `EatClubError`.

```python
from eatclub.exceptions import EatClubError, EatClubAuthError, EatClubAPIError

try:
    # Any API call
    client.customer.get_profile()
except EatClubAuthError:
    # Handle bad/expired auth token
    pass
except EatClubAPIError as e:
    # e.status_code and e.payload are available
    print(f"Error {e.status_code}: {e.payload}")
except EatClubError:
    # Generic fallback for any other package error
    pass
```
