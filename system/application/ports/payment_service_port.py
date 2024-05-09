from abc import abstractmethod


class PaymentServicePort:
    @classmethod
    @abstractmethod
    def create_payment(cls, value: str) -> str:
        """
        Create Payment and returns payment id
        """

