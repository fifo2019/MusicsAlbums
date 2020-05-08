import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
        Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find_artist():
    """
        Находит всеx артистев
    """
    SESSION = connect_db()
    artist = SESSION.query(Album.artist).group_by(Album.artist).all()
    return artist

def find_album(artist):
    """
        Находит все альбомы в базе данных по заданному артисту
    """
    SESSION = connect_db()
    albums = SESSION.query(Album).filter(Album.artist == artist).all()
    return albums


def add_album(album):
    SESSION = connect_db()
    SESSION.add(album)
    SESSION.commit()
    return True


def check_record(data):
    SESSION = connect_db()
    find_coincidences = SESSION.query(Album).filter(
        Album.year == data.get('year'), Album.artist == data.get('artist'),
        Album.genre == data.get('genre'), Album.album == data.get('album')
    ).first()

    if find_coincidences is None:
        album = Album(
            year=data.get('year'),
            artist=data.get('artist'),
            genre=data.get('genre'),
            album=data.get('album'),
        )

        return album
    else:
        return False