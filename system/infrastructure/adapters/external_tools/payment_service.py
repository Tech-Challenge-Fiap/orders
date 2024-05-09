from system.application.ports.payment_service_port import PaymentServicePort
import requests
import json


class PaymentService(PaymentServicePort):
    @classmethod
    def create_payment(cls, value) -> str:
        """
        Create Payment and returns payment_id
        """
        url = "http://localhost:5003/create_payment"
        payload = {
            "value": str(value)
        }
        response = requests.request("POST", url, json=payload)
        response_json = response.json()
        return response_json["id"]
