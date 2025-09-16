from .extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TokenBlocklist(db.Model):
    __tablename__ = "revoked_tokens"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jti: Mapped[str] = mapped_column(db.String(36), nullable=False, index=True)
    createdAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now())

    def __repr__(self) -> str:
        return f"<Token {self.jti}>"

class User(db.Model):
    __tablename__ = "users"
    
    id:            Mapped[int]         = mapped_column(db.Integer, primary_key=True)
    username:      Mapped[str]         = mapped_column(db.String(50), unique=True, nullable=False)
    email:         Mapped[str]         = mapped_column(db.String(100), unique=True, nullable=False)
    password_hash: Mapped[str]         = mapped_column(db.String(256), nullable=False)
    firstName:     Mapped[str]         = mapped_column(db.String(50), nullable=True)
    lastName:      Mapped[str]         = mapped_column(db.String(70), nullable=True)
    isAdmin:       Mapped[bool]        = mapped_column(db.Boolean, default=False)
    
    # datetime.now().strftime("%A %H:%M %d/%m/%Y") <- better format
    createdAt:     Mapped[datetime]    = mapped_column(db.DateTime, default=lambda: datetime.now())
                                                            #  server_default=db.func.now() also works

    # relationship to dashboard
    # `uselist=False` -> one-to-one relationship
    dashboard:     Mapped["Dashboard"] = relationship(back_populates="user", uselist=False)

    def __init__(self, username: str, email: str, password: str, firstName: str = None, lastName: str = None, isAdmin: bool = False) -> None:
        super().__init__()
        
        self.username   = username
        self.email      = email
        self.firstName = firstName
        self.lastName  = lastName
        self.isAdmin   = isAdmin
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def serialize(self) -> dict:
        return {
            "id":         self.id,
            "username":   self.username,
            "firstName":  self.firstName if self.firstName else None,
            "lastName":   self.lastName if self.lastName else None,
            "createdAt":  self.createdAt.isoformat() if self.createdAt else None,
            "dashboard":  self.dashboard.serialize()
        }
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"

class Dashboard(db.Model):
    __tablename__ = "dashboards"

    id:             Mapped[int]             = mapped_column(db.Integer, primary_key=True)
    userId:         Mapped[int]             = mapped_column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    dashboardName:  Mapped[str]             = mapped_column(db.String(100), unique=False, nullable=False)

    createdAt:      Mapped[datetime]        = mapped_column(db.DateTime, default=lambda: datetime.now())

    # relationships
    user:           Mapped["User"]          = relationship(back_populates="dashboard")
    products:       Mapped[list["Product"]] = relationship(back_populates="dashboard")
    sales:          Mapped[list["Venda"]]   = relationship(back_populates="dashboard")

    def serialize(self) -> dict:
        return {
            "id":            self.id,
            "userId":        self.userId,
            "createdAt":     self.createdAt.isoformat() if self.createdAt else None,
            "dashboardName": self.dashboardName
        }
    
    def __repr__(self) -> str:
        return f"<Dashboard(id={self.id}, name='{self.dashboardName}')>"

class Product(db.Model):
    __tablename__ = "products"
    
    id:              Mapped[int]           = mapped_column(db.Integer, primary_key=True)
    dashboardId:     Mapped[int]           = mapped_column(db.Integer, ForeignKey("dashboards.id"), nullable=False)

    productName:     Mapped[str]           = mapped_column(db.String(100), nullable=False)
    productImage:    Mapped[str]           = mapped_column(db.Text, nullable=True)

    isDeleted:       Mapped[bool]          = mapped_column(db.Boolean, default=False)

    productPrice:    Mapped[float]         = mapped_column(db.Float, nullable=False)
    productCost:     Mapped[float]         = mapped_column(db.Float, nullable=True)
    productBarcode:  Mapped[str]           = mapped_column(db.String(14), nullable=True)
    productStock:    Mapped[int]           = mapped_column(db.Integer, default=0)

    createdAt:       Mapped[datetime]      = mapped_column(db.DateTime, default=lambda: datetime.now())

    # relationships
    dashboard:       Mapped["Dashboard"]   = relationship(back_populates="products")
    sales:           Mapped[list["Venda"]] = relationship(back_populates="product")

    # table args - make product_name and product_barcode unique ONLY on the dashboard
    __table_args__ = (
        UniqueConstraint("dashboardId", "productName", name="_dashboard_product_name_uc"),
        # UniqueConstraint("dashboardId", "productBarcode", name="_dashboard_product_barcode_uc")
    )

    def serialize(self) -> dict:
        return {
            "productId":      self.id,
            "dashboardId":    self.dashboardId,
            "productName":    self.productName,
            "productPrice":   self.productPrice,
            "productImage":   self.productImage,
            "productBarcode": self.productBarcode,
            "productStock":   self.productStock,
            "createdAt":      self.createdAt.isoformat() if self.createdAt else None,
            "productCost":    self.productCost,
            "isDeleted":      self.isDeleted,
        }

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, productName='{self.productName}')>"

class Venda(db.Model):
    __tablename__ = "vendas"

    id:          Mapped[int]         = mapped_column(db.Integer, primary_key=True)
    productId:   Mapped[int]         = mapped_column(db.Integer, ForeignKey("products.id"), nullable=False)
    dashboardId: Mapped[int]         = mapped_column(db.Integer, ForeignKey("dashboards.id"), nullable=False)
    soldAmount:  Mapped[int]         = mapped_column(db.Integer, default=1)
    priceAtSale: Mapped[float]       = mapped_column(db.Float, nullable=False)
    costAtSale:  Mapped[float]       = mapped_column(db.Float, nullable=True)
    soldAt:      Mapped[datetime]    = mapped_column(db.DateTime, default=lambda: datetime.now())

    description:  Mapped[str]        = mapped_column(db.String(250), nullable=True)

    # relationships
    product:     Mapped["Product"]   = relationship(back_populates="sales")
    dashboard:   Mapped["Dashboard"] = relationship(back_populates="sales")

    def __repr__(self) -> str:
        return f"<Venda(id={self.id}, productId={self.productId})>"
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "productId": self.productId,
            "product": self.product.serialize(),
            "dashboardId": self.dashboardId,
            "description": self.description,
            "soldAmount": self.soldAmount,
            "priceAtSale": self.priceAtSale,
            "costAtSale": self.costAtSale,
            "soldAt": self.soldAt.isoformat() if self.soldAt else None
        }
