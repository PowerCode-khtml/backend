"""
상점 결제 방법 모델
"""
from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StorePaymentMethod(Base):
    __tablename__ = "storePaymentMethod"
    
    payentMethodid = Column(Integer, ForeignKey("paymentMethod.payentMethodid"), primary_key=True)
    storeid = Column(BigInteger, ForeignKey("store.storeid"), primary_key=True)
    
    # 관계 정의
    payment_method = relationship("PaymentMethod", back_populates="store_methods")
    store = relationship("Store")  # 단순화
