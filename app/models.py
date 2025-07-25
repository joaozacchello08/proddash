from .extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from passlib.hash import bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id:            Mapped[int]  = mapped_column(db.Integer, primary_key=True)
    username:      Mapped[str]  = mapped_column(db.String(50), unique=False, nullable=False)
    email:         Mapped[str]  = mapped_column(db.String(100), unique=True, nullable=False)
    password_hash: Mapped[str]  = mapped_column(db.String(128), nullable=False)
    first_name:    Mapped[str]  = mapped_column(db.String(30), nullable=True)
    last_name:     Mapped[str]  = mapped_column(db.String(50), nullable=True)
    is_admin:      Mapped[bool] = mapped_column(db.Boolean, default=False)
    
    # datetime.now().strftime("%A %H:%M %d/%m/%Y") <- better format
    created_at:    Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now())

    def __init__(self, username: str, email: str, password: str, first_name: str = None, last_name: str = None, is_admin: bool = False):
        super().__init__()
        
        self.username   = username
        self.email      = email
        self.first_name = first_name
        self.last_name  = last_name
        self.is_admin   = is_admin
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)
    
    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    def serialize(self) -> dict:
        return {
            "id":         self.id,
            "username":   self.username,
            "firstName":  self.first_name,
            "lastName":   self.last_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"

class Dashboard(db.Model):
    __tablename__ = "dashboards"

    id:             Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id:        Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    dashboard_name: Mapped[str] = mapped_column(db.String(30), unique=False, nullable=False)

    created_at:     Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now())

    def __init__(self, user_id: str, dashboard_name: str):
        super().__init__()

        self.user_id        = user_id
        self.dashboard_name = dashboard_name

    def serialize(self) -> dict:
        return {
            "id":             self.id,
            "user_id":        self.user_id,
            "created_at":     self.created_at.isoformat() if self.created_at else None,
            "dashboard_name": self.dashboard_name
        }
    
    def __repr__(self) -> str:
        return f"<Dashboard(id={self.id}, name='{self.dashboard_name}')>"

class Product(db.Model):
    __tablename__ = "products"
    
    id:              Mapped[int] = mapped_column(db.Integer, primary_key=True)
    dashboard_id:    Mapped[int] = mapped_column(db.Integer, db.ForeignKey("dashboards.id"))

    product_name:    Mapped[str]   = mapped_column(db.String(32), unique=True, nullable=False)
    product_image:   Mapped[str]   = mapped_column(db.Text, nullable=True)
    product_price:   Mapped[float] = mapped_column(db.Float, nullable=False)
    product_barcode: Mapped[str]   = mapped_column(db.String(14), unique=True, nullable=True)
    product_stock:   Mapped[int]   = mapped_column(db.Integer, default=0)

    created_at:      Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now())

    def __init__(self, product_name: str, product_stock: int, product_price: float, product_image: str = None, product_barcode: str = None):
        super().__init__()
        
        self.product_name    = product_name
        self.product_stock   = product_stock
        self.product_price   = product_price
        self.product_image   = product_image
        self.product_barcode = product_barcode

    def serialize(self):
        return {
            "product_id":      self.id,
            "product_name":    self.product_name,
            "product_price":   self.product_price,
            "product_image":   self.product_image,
            "product_barcode": self.product_barcode,
            "product_stock":   self.product_stock,
            "created_at":      self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, product_name='{self.product_name}')>"
