from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


DATABASE_URL = "postgresql://pc:1122@localhost:5432/home_db"

BaseModel = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(bind=engine)


class City(BaseModel):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    name_city = Column(String)
    days_delivery = Column(Integer)

    def __repr__(self):
        return f'Город {self.name_city}, срок доставки: {self.days_delivery}'


class Author(BaseModel):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    name_author = Column(String)

    def __repr__(self):
        return f'Автор "{self.name_author}".'


class Book(BaseModel):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Integer)
    amount = Column(Integer)

    def __repr__(self):
        info: str = f'Книга "{self.title}" автора {self.author_id}.' \
            f'Количество страниц: {self.amount}. Цена: {self.price}.'
        return info


class BuyBook(BaseModel):
    __tablename__ = 'buy_book'

    buy_book_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    amount = Column(Integer)


class BuyStep(BaseModel):
    __tablename__ = 'buy_step'

    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))
    date_step_beg = Column(DateTime(timezone=True))
    date_step_end = Column(DateTime(timezone=True))


class Buy(BaseModel):
    __tablename__ = 'buy'

    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String)
    client_id = Column(Integer, ForeignKey('client.client_id'))


class Client(BaseModel):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    name_client = Column(String)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String)


class Genre(BaseModel):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String)

    def __repr__(self):
        return f'Название жанра: {self.name_genre}'


class Step(BaseModel):
    __tablename__ = 'step'

    step_id = Column(Integer, primary_key=True)
    name_step = Column(String)


def create_db():
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
