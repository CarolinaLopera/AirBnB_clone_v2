#!/usr/bin/python3
"""Database storage airbnb"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """create the engine"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name (argument cls)"""
        if cls is None:
            clslist = [City, Place, State, User, Amenity, Review]
            temp = {}
            for index in clslist:
                objlist = self.__session.query(eval(index))
                for j in objlist:
                    k = "{}.{}".format(type(j).__name__, j.id)
                    temp[k] = j
        else:
            temp = {}
            if type(cls) == str:
                cls = eval(cls)
            objlist = self.__session.query(cls)
            for index in objlist:
                k = "{}.{}".format(type(index).__name__, index.id)
                temp[k] = index
        return temp

    def new(self, obj):
        """add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """save the object to the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """delete the object to the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(expire_on_commit=False,
                                              bind=self.__engine))
        self.__session = Session()
