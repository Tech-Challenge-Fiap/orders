from enum import Enum


class OrderStatusEnum(str, Enum):
    CANCELED = "CANCELED"
    TO_BE_PAYED = "WAITING PAYMENT"
    RECIEVED = "RECIEVED"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"
