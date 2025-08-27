"""
결제 수단 스키마
"""
from pydantic import BaseModel

class PaymentMethodBase(BaseModel):
    paymentMethodName: str

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    paymentMethodid: int

    class Config:
        from_attributes = True
