"""
결제 방법 모델
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class PaymentMethod(Base):
    __tablename__ = "paymentMethod"
    
    payentMethodid = Column(Integer, primary_key=True, autoincrement=True)
    paymentMethodName = Column(String(30), nullable=False)
    
    # 관계 정의
    store_methods = relationship("StorePaymentMethod", back_populates="payment_method")
