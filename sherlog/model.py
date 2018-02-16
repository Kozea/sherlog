from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'

    return_code = Column(Integer, nullable=True)
    message = Column(String, nullable=False)
    url = Column(String, nullable=True)
    ok = Column(Boolean, nullable=False)
    host = Column(String, nullable=True, index=True)
    start = Column(DateTime, primary_key=True)
    stop = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    stderr = Column(String, nullable=True)
    stdout = Column(String, nullable=True)
    command = Column(String, nullable=True)

    server_name = Column(String, nullable=False, index=True)
