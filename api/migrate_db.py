from sqlalchemy import create_engine

from api.models.task import Base

DB_URL = "postgresql://guest:password@localhost:5432/my-db"
engine = create_engine(DB_URL, echo=True)


def reset_database():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
  reset_database()
