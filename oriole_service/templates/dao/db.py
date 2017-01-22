from oriole_service.db import *


class Users(Base):
    __tablename__ = 'users'
    id_ai = Column(types.Integer(), primary_key=True, autoincrement=True)
    name = Column(types.Unicode(255), nullable=False, unique=None, default='')
    add_time = Column(types.DateTime(), default='0000-00-00 00:00:00')
    add_time_int = Column(types.Integer(), nullable=True, default=0)
