from .extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from passlib.hash import bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id:            Mapped[int]         = mapped_column(db.Integer, primary_key=True)
    username:      Mapped[str]         = mapped_column(db.String(50), unique=True, nullable=False)
    email:         Mapped[str]         = mapped_column(db.String(100), unique=True, nullable=False)
    password_hash: Mapped[str]         = mapped_column(db.String(128), nullable=False)
    first_name:    Mapped[str]         = mapped_column(db.String(30), nullable=True)
    last_name:     Mapped[str]         = mapped_column(db.String(50), nullable=True)
    is_admin:      Mapped[bool]        = mapped_column(db.Boolean, default=False)
    
    # datetime.now().strftime("%A %H:%M %d/%m/%Y") <- better format
    created_at:    Mapped[datetime]    = mapped_column(db.DateTime, default=lambda: datetime.now())
                                                            #  server_default=db.func.now() also works

    # relationship to dashboard
    # `uselist=False` -> one-to-one relationship
    dashboard:     Mapped["Dashboard"] = relationship(back_populates="user", uselist=False)

    def __init__(self, username: str, email: str, password: str, first_name: str = None, last_name: str = None, is_admin: bool = False) -> None:
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
            "createdAt":  self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"

class Dashboard(db.Model):
    __tablename__ = "dashboards"

    id:             Mapped[int]             = mapped_column(db.Integer, primary_key=True)
    user_id:        Mapped[int]             = mapped_column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    dashboard_name: Mapped[str]             = mapped_column(db.String(30), unique=False, nullable=False)

    created_at:     Mapped[datetime]        = mapped_column(db.DateTime, default=lambda: datetime.now())

    # relationships
    user:           Mapped["User"]          = relationship(back_populates="dashboard")
    products:       Mapped[list["Product"]] = relationship(back_populates="dashboard")
    sales:          Mapped[list["Venda"]]   = relationship(back_populates="dashboard")

    # everything already mapped and will be assigned manually, so __init__ method is kinda useless
    # def __init__(self, user_id: str, dashboard_name: str) -> None:
    #     super().__init__()

    #     self.user_id        = user_id
    #     self.dashboard_name = dashboard_name

    def serialize(self) -> dict:
        return {
            "id":            self.id,
            "userId":        self.user_id,
            "createdAt":     self.created_at.isoformat() if self.created_at else None,
            "dashboardName": self.dashboard_name
        }
    
    def __repr__(self) -> str:
        return f"<Dashboard(id={self.id}, name='{self.dashboard_name}')>"

class Product(db.Model):
    __tablename__ = "products"
    
    id:              Mapped[int]           = mapped_column(db.Integer, primary_key=True)
    dashboard_id:    Mapped[int]           = mapped_column(db.Integer, ForeignKey("dashboards.id"), nullable=False)

    product_name:    Mapped[str]           = mapped_column(db.String(32), unique=True, nullable=False)
    product_image:   Mapped[str]           = mapped_column(db.Text, nullable=True)

    product_price:   Mapped[float]         = mapped_column(db.Float, nullable=False)
    product_cost:    Mapped[float]         = mapped_column(db.Float, nullable=True)
    product_barcode: Mapped[str]           = mapped_column(db.String(14), unique=True, nullable=True)
    product_stock:   Mapped[int]           = mapped_column(db.Integer, default=0)

    created_at:      Mapped[datetime]      = mapped_column(db.DateTime, default=lambda: datetime.now())

    # relationships
    dashboard:       Mapped["Dashboard"]   = relationship(back_populates="products")
    sales:           Mapped[list["Venda"]] = relationship(back_populates="product")

    # ...
    # def __init__(self, product_name: str, product_stock: int, product_price: float, product_image: str = None, product_barcode: str = None) -> None:
    #     super().__init__()
        
    #     self.product_name    = product_name
    #     self.product_stock   = product_stock
    #     self.product_price   = product_price
    #     self.product_image   = product_image
    #     self.product_barcode = product_barcode

    def serialize(self) -> dict:
        return {
            "productId":      self.id,
            "productName":    self.product_name,
            "productPrice":   self.product_price,
            "productImage":   self.product_image,
            "productBarcode": self.product_barcode,
            "productStock":   self.product_stock,
            "createdAt":      self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, product_name='{self.product_name}')>"

class Venda(db.Model):
    __tablename__ = "vendas"

    id:            Mapped[int]         = mapped_column(db.Integer, primary_key=True)
    product_id:    Mapped[int]         = mapped_column(db.Integer, ForeignKey("products.id"), nullable=False)
    dashboard_id:  Mapped[int]         = mapped_column(db.Integer, ForeignKey("dashboards.id"), nullable=False)
    sold_amount:   Mapped[int]         = mapped_column(db.Integer, default=1)
    price_at_sale: Mapped[float]       = mapped_column(db.Float, nullable=False)
    cost_at_sale:  Mapped[float]       = mapped_column(db.Float, nullable=True)
    sold_at:       Mapped[datetime]    = mapped_column(db.DateTime, default=lambda: datetime.now())

    # relationships
    product:       Mapped["Product"]   = relationship(back_populates="sales")
    dashboard:     Mapped["Dashboard"] = relationship(back_populates="sales")

    # ...
    # def __init__(self, product_id: int, sold_amount: int = 1) -> None:
    #     super().__init__()

    #     self.product_id = product_id
    #     self.sold_amount = sold_amount

    def __repr__(self) -> str:
        return f"<Venda(id={self.id}, product_id={self.product_id})>"
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "productId": self.product_id,
            "dashboardId": self.dashboard_id,
            "soldAmount": self.sold_amount,
            "priceAtSale": self.price_at_sale,
            "costAtSale": self.cost_at_sale,
            "soldAt": self.sold_at.isoformat() if self.sold_at else None
        }
