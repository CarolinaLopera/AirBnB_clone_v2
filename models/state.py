#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """ File storage city getter """
            city_list = models.storage.all(City)
            temp = []
            for city in list(city_list.values()):
                if city.state_id == self.id:
                    temp.append(city)
            return temp
