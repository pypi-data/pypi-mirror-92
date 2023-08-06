from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine("sqlite+pysqlite:///doc.db", echo=True, future=True)
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/doc.db',
                       echo=True,
                       future=True,
                       echo_pool='debug',
                       logging_name='doc-db-engine')


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



if __name__ == '__main__':
    next(get_db())