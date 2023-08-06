"""Wasilliana API Client for wasiliana.com."""
import requests

__version__ = "0.0.1"
__author__ = "Tralah M Brian"
__author_email__ = "briantralah@gmail.com"
__project_url__ = "https://github.com/TralahM/pytek-wasiliana"
__package_name__ = "pytek-wasiliana"


class APIClient:
    """Wasiliana API Client."""

    example_delivery = {
        "phone": "25472x xxx xxx",
        "correlator": "message_15883801465eacc1f2643a9",
        "deliveryStatus": "0",
        "failure_reason": "",
    }
    example_callback = {
        "recipients": ["25472x xxx xxx"],
        "from": "company-x",
        "message": "Reply to ....",
        "linkid": "requred field",
    }

    def __init__(self, apiKey, *args, **kwargs):
        """Create API Client Instance."""
        self.apiKey = apiKey

    def _execute(self, url, payload):
        """Execute Network Request to the url with the payload."""
        headers = {
            "Content-Type": "application/json",
            "apiKey": self.apiKey,
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def send_sms(self, sender_id: str, recipients=[], message=""):
        """Send sms message from senderId to recipients."""
        url = "https://api.wasiliana.com/api/v1/developer/send/sms"
        payload = {
            "recipients": recipients,
            "from": sender_id,
            "message": message,
        }
        return self._execute(url, payload)

    def send_bulk_sms(self, sender_id: str, recipients=[], message=""):
        """Send bulk sms message from senderId to recipients."""
        url = "https://api.wasiliana.com/api/v1/developer/sms/bulk/send/sms/request"
        payload = {
            "recipients": recipients,
            "from": sender_id,
            "message": message,
        }
        return self._execute(url, payload)
