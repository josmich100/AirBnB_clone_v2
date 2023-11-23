#!/usr/bin/python3
"""This is the Amenity class"""
from os import getenv
from models.base_model import BaseModel, Base
from models.place import Place
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

class Amenity(BaseModel, Base):
    """This class represents an Amenity in the system.

    Attributes:
        name (str): The name of the Amenity.
    """
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        # Define a relationship with Place through the association table 'place_amenity'
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            viewonly=False,
            back_populates="amenities"
        )
