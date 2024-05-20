from system.application.ports.payment_service_port import PaymentServicePort
import requests


class PaymentService(PaymentServicePort):
    @classmethod
    def create_payment(cls, value) -> str:
        """
        Create Payment and returns payment_id
        """
        url = "http://payment-svc:5000/create_payment"
        payload = {
            "value": str(value)
        }
        response = requests.request("POST", url, json=payload)
        response_json = response.json()
        return response_json["id"]
