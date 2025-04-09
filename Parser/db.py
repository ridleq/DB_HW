from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func


DATABASE_URL = "postgresql://pc:1122@localhost:5432/parse_db"

BaseModel = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
if not database_exists(engine.url):
    create_database(engine.url)

BaseModel.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


class TradeRes(BaseModel):
    __tablename__ = 'trade_result'

    id = Column(Integer, primary_key=True)
    exchange_product_id = Column(String, index=True)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Float)
    total = Column(Float)
    count = Column(Integer)
    date = Column(DateTime)
    created_on = Column(DateTime, default=func.now)
    updated_on = Column(
        DateTime, default=func.now, onupdate=func.now
    )


def create_db():
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
