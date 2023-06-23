import numpy as np
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///../data/data.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session = SessionLocal()


class Operator(Base):
    __tablename__ = "data"
    id = Column(Integer, index=True, primary_key=True)
    tt = Column(Integer)
    tm = Column(Integer)
    tf = Column(Integer)
    mt = Column(Integer)
    mm = Column(Integer)
    mf = Column(Integer)
    ft = Column(Integer)
    fm = Column(Integer)
    ff = Column(Integer)
    count = Column(Integer)

    @classmethod
    def query_by_pattern(cls, *args):
        return (
            session.query(Operator)
            .filter(
                Operator.tt == args[0],
                Operator.tm == args[1],
                Operator.tf == args[2],
                Operator.mt == args[3],
                Operator.mm == args[4],
                Operator.mf == args[5],
                Operator.ft == args[6],
                Operator.fm == args[7],
                Operator.ff == args[8],
            )
            .first()
        )

    @classmethod
    def query_by_str(cls, s: str):
        return Operator.query_by_pattern(*[int(item) for item in s.split(",")])

    @classmethod
    def query_by_array(cls, arr: np.ndarray):
        return Operator.query_by_pattern(*arr.reshape(9).tolist())

    def __str__(self) -> str:
        return f"{self.tt},{self.tm},{self.tf},{self.mt},{self.mm},{self.mf},{self.ft},{self.fm},{self.ff}"

    def to_tuple(self) -> tuple:
        return (self.tt, self.tm, self.tf, self.mt, self.mm, self.mf, self.ft, self.fm, self.ff)

    def to_array(self):
        return np.array(
            [
                [self.tt, self.tm, self.tf],
                [self.mt, self.mm, self.mf],
                [self.ft, self.fm, self.ff],
            ]
        )


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    with open("../data/output", "r") as f:
        lines = f.readlines()

    for line in lines:
        (index, mapping, counter) = line[:-1].split("|")

        data = Operator()
        data.id = int(index.split(" ")[0])
        (data.tt, data.tm, data.tf, data.mt, data.mm, data.mf, data.ft, data.fm, data.ff) = (
            mapping.replace("[", "").replace("]", "").split(" ")
        )
        data.count = int(counter)

        session.add(data)

    session.commit()
