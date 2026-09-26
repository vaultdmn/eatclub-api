<div align="center">
  <h1>🍕 EatClub / Box8 API Python Client 🍔</h1>
  
  <p><strong>Unofficial Python wrapper for the EatClub (Box8) Android App API</strong></p>

  <p>
    <a href="https://badge.fury.io/py/eatclub"><img src="https://badge.fury.io/py/eatclub.svg" alt="PyPI version" height="18"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
    <a href="https://github.com/psf/requests"><img src="https://img.shields.io/badge/dependencies-requests-brightgreen.svg" alt="Dependencies"></a>
  </p>
  <p>
    <i>Explore menus, manage your cart, apply offers, and track your food orders completely via Python.</i>
  </p>
</div>

---

## ✨ Features

- **🛡️ Easy Authentication:** Built-in OTP based login flow for EatClub.
- **🌮 Full Catalog Access:** Browse brands, locations, and real-time outlet menus.
- **🛒 Shopping Cart Management:** Build carts, apply promo codes, and validate checkouts.
- **📦 Order Tracking:** Fetch order history and active live-tracking details.
- **🧩 Fluent Interface:** Organized into sub-modules (`auth`, `catalog`, `cart`, `customer`, `order`) for easy navigation.
- **🚨 Typed Exceptions:** Clean error handling with custom exceptions.

## 🛠️ Installation

You can install the package by downloading the source and using `pip`:

```bash
# Clone the repository or navigate to the folder
git clone https://github.com/yourusername/eatclub-api.git
cd eatclub-api

# Install dependencies and the package
pip install .
```

## 🚀 Quick Start & Authentication

The EatClub API requires token-based authentication. You can seamlessly authenticate using your phone number via OTP.

```python
from eatclub import EatClubClient

# 1. Initialize the client
client = EatClubClient()

# 2. Request OTP to your phone
phone_number = "9876543210"
client.auth.request_otp(phone_number)
print("OTP sent to your phone!")

# 3. Enter the OTP to lock in the session
otp = input("Enter OTP: ")
client.auth.verify_otp(phone_number, otp)

# 🎉 You are now authenticated!
```

> **Pro-Tip:** If you already have your EatClub Auth Token, you can bypass the OTP process:
> ```python
> client = EatClubClient(token="YOUR_EATCLUB_TOKEN_HERE")
> ```

---

## 📖 Module Usage Guide

Once authenticated, you have access to a variety of modules attached to the `client`. Here is how you can use them:

### 1. Catalog (`client.catalog`)
Quickly fetch nearby outlets and explore menus based on your GPS coordinates.

```python
# Setup your location
lat, lon = "28.513188", "77.077349"

# Fetch nearby restaurants / outlets
outlets = client.catalog.get_outlets(lat=lat, lon=lon)
for outlet in outlets.get("outlet", []):
    print(f"Outlet: {outlet['name']} | Status: {outlet['status']}")

# Fetch the menu for a specific outlet
menu = client.catalog.get_products(outlet_id="353")
print("Menu Options:", menu.get("menus", []))
```

### 2. Customer (`client.customer`)
Manage your personal profile and saved addresses.

```python
# Get basic profile info
profile = client.customer.get_profile()
print(f"Logged in as: {profile.get('name')}")

# Get saved delivery addresses
addresses = client.customer.get_addresses()
```

### 3. Cart & Offers (`client.cart`)
Programmatically create a cart and add items to it.

```python
# Add parameters to start a cart checkout
cart_data = client.cart.get_cart(
    lat="28.513188", 
    lon="77.077349",
    cart_items=[
        {"item_id": "9945", "quantity": 1}
    ]
)

# Fetch current credit balance
credit = client.cart.get_credit_balance()
print(f"EatClub Wallet Balance: ₹{credit.get('credit_balance', 0)}")
```

### 4. Orders (`client.order`)
Keep track of previous and live orders.

```python
# Fetch page 1 of order history
history = client.order.get_orders(page=1)
print(history.get('customer_orders'))

# Track an active live order using Tracking ID
tracking = client.order.get_tracking_details(tracking_id="TRK12345", outlet_id="353")
```

---

## ⚠️ Exception Handling

The package provides custom exceptions located in `eatclub.exceptions` to help you smoothly capture and handle API faults.

```python
from eatclub import EatClubClient, EatClubAPIError, EatClubAuthError

client = EatClubClient()

try:
    client.customer.get_profile()
except EatClubAuthError as e:
    print("Authentication Failed. Please login via OTP first.")
except EatClubAPIError as e:
    print(f"API Failed with status {e.status_code}: {str(e)}")
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](#) to see open tickets.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚖️ Disclaimer & Legal

This is an **unofficial** educational tool and is completely unaffiliated with Box8, EatClub, or their parent companies. The use of this wrapper is entirely at your own risk. The developer holds no liability for account bans, damages, or breaches of terms of service. Please respect rate limits and terms of service guidelines established by EatClub.
