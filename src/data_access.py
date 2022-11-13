from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

class DataAccess:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")


    def insert(self, object):
        with Session(self.engine) as session:
            session.add(object)
            session.commit()
    

    def select_all(self, table):
        with Session(self.engine) as session:
            return list(session.scalars(select(table)))


    def select_one_by(self, table, condition):
        with Session(self.engine) as session:
            return session.scalar(select(table).where(condition))


    def select_all_by(self, table, condition):
        with Session(self.engine) as session:
            return list(session.scalars(select(table).where(condition)))


    def select_size_by(self, table, condition):
        with Session(self.engine) as session:
            return session.scalar(
                select(func.count(inspect(table).primary_key)).where(condition))
