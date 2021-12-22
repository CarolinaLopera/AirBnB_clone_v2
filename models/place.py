#!/usr/bin/python3
""" Place Module for HBNB project """
import os
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Table
from sqlalchemy.orm import relationship


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False)
    if os.getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Getter reviews"""
            review = []
            for i in list(models.storage.all(Review).values()):
                if i.place_id == self.id:
                    review .append(i)
            return review

        @property
        def amenities(self):
            """Getter amenities"""
            amenity = []
            for i in list(models.storage.all(Amenity).values()):
                if i.id == self.amenity_ids:
                    amenity.append(i)
            return amenity

        @amenities.setter
        def amenities(self, obj):
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
