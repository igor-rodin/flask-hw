from databases import Database
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Table,
    DECIMAL,
    DateTime,
    Boolean,
    ForeignKey,
    create_engine,
)
from settings import settings


db = Database(settings.DATABASE_URL)
metadata = MetaData()

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(settings.NAME_MAX_LENGTH)),
    Column("last_name", String(settings.NAME_MAX_LENGTH)),
    Column("email", String(settings.EMAIL_MAX_LENGTH)),
    Column("password", String(128)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_name", String(settings.NAME_MAX_LENGTH)),
    Column("description", String(settings.NAME_MAX_LENGTH)),
    Column("price", DECIMAL(8, 2)),
)

order_status = Table(
    "order_status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("status_name", String(settings.NAME_MAX_LENGTH)),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("order_date", DateTime, nullable=False),
    Column("order_status", Integer, ForeignKey("order_status.id"), nullable=False),
    Column("products_amount", Integer, nullable=False),
)

metadata.create_all(engine)
