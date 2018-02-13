import datetime
import time

from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unrest import UnRest

from sherlog import model


class Sherlog(Flask):
    def create_session(self):
        return sessionmaker(bind=create_engine(self.config['DB']))()

    def before(self):
        g.session = self.create_session()

    def initialize(self):
        self.before_request(self.before)

        rest = UnRest(self, self.create_session())

        rest(model.Log, methods=['GET'])
