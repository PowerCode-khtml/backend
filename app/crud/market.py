from sqlalchemy.orm import Session
from app.models import market as market_model

def get_markets(db: Session):
    return db.query(market_model.Market).all()
