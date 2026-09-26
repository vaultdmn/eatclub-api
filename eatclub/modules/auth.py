from . import BaseModule

class AuthModule(BaseModule):
    BASE_URL = "https://accounts.box8.co.in/customers"

    def request_otp(self, phone_no: str) -> dict:
        """
        Initiate login by sending an OTP to the given phone number.
        Returns the response metadata.
        """
        # First check phone status (as the app does)
        self._client.request("POST", f"{self.BASE_URL}/check_phone_status", json={"phone_no": phone_no})

        # Then request the OTP
        payload = {
            "initiate": "true",
            "phone_no": phone_no,
            "login_method": "otp"
        }
        return self._client.request("POST", f"{self.BASE_URL}/sign_in", json=payload)

    def verify_otp(self, phone_no: str, otp: str, set_token: bool = True) -> dict:
        """
        Verify the OTP and return the authentication data.
        If set_token is True, updates the client's session with the new token.
        """
        payload = {
            "initiate": "false",
            "phone_no": phone_no,
            "login_method": "otp",
            "otp": otp
        }

        data = self._client.request("POST", f"{self.BASE_URL}/sign_in", json=payload)

        # The token is usually in data['customer']['token'] or similar. We need to check structure.
        # Assuming typical box8 response structure based on common patterns.
        # Let's inspect the actual response structure for sign_in if possible, but standard is customer -> token
        # If set_token is true, we configure the client.
        if set_token and "customer" in data and "token" in data["customer"]:
            self._client.set_token(data["customer"]["token"])

        return data
