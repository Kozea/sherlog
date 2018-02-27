from sqlalchemy import Boolean, Column, DateTime, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'

    return_code = Column(Integer, nullable=True)
    message = Column(Unicode, nullable=False)
    url = Column(Unicode, nullable=True)
    ok = Column(Boolean, nullable=False)
    host = Column(Unicode, nullable=True, index=True)
    start = Column(DateTime, primary_key=True)
    stop = Column(DateTime, nullable=False)
    status = Column(Unicode, nullable=False)

    stderr = Column(Unicode, nullable=True)
    stdout = Column(Unicode, nullable=True)
    command = Column(Unicode, nullable=True)

    server_name = Column(Unicode, nullable=False, index=True)
