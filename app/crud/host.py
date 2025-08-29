"""
호스트 CRUD 작업
"""
from sqlalchemy.orm import Session
from app.models.host import Host
from app.schemas.host import HostCreate
from app.services.auth import AuthService

def get_host(db: Session, host_id: int):
    return db.query(Host).filter(Host.hostid == host_id).first()

def get_host_by_email(db: Session, email: str):
    return db.query(Host).filter(Host.email == email).first()

def get_hosts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Host).offset(skip).limit(limit).all()

def create_host(db: Session, host: HostCreate):
    hashed_password = AuthService.get_password_hash(host.password)
    db_host = Host(
        email=host.email,
        name=host.name,
        password=hashed_password,
    )
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

def authenticate_host(db: Session, email: str, password: str):
    host = get_host_by_email(db, email)
    if not host:
        return False
    if not AuthService.verify_password(password, host.password):
        return False
    return host
