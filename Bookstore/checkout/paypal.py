import os
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        # Retrieve client ID and secret from environment variables
        self.client_id = os.getenv('PAYPAL_CLIENT_ID')
        self.client_secret = os.getenv('PAYPAL_CLIENT_SECRET')

        # Create a sandbox environment
        self.environment = SandboxEnvironment(
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        # Initialize PayPal client
        self.client = PayPalHttpClient(self.environment)


