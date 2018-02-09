from flask import Flask
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Sherlog(Flask):
    def create_session(self):
        return sessionmaker(bind=create_engine(self.config['DB']))()

    def before(self):
        g.session = self.create_session()

    def initialize(self):
        self.before_request(self.before)
