#!/usr/bin/python3
"""This is the base model class for AirBnB"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """This class defines common attributes/methods for other classes."""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        else:
            self.set_attributes(kwargs)

    def set_attributes(self, kwargs):
        """Set attributes from provided keyword arguments."""
        date_keys = ["created_at", "updated_at"]
        for key, value in kwargs.items():
            if key in date_keys:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            if key != "__class__":
                setattr(self, key, value)

        if "id" not in kwargs:
            self.id = str(uuid.uuid4())
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
        if "updated_at" not in kwargs:
            self.updated_at = datetime.now()

    def __str__(self):
        """Return a string representation."""
        return f"[{type(self).__name__}] ({self.id}) {self.to_dict()}"

    def __repr__(self):
        """Return a string representation."""
        return self.__str__()

    def save(self):
        """Update the public instance attribute updated_at to current."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Create dictionary representation of the class."""
        my_dict = {
            key: value.isoformat() if isinstance(value, datetime) else value
            for key, value in self.__dict__.items()
            if key != "_sa_instance_state"
        }
        my_dict["__class__"] = str(type(self).__name__)
        return my_dict

    def delete(self):
        """Delete current instance from the storage (models.storage)."""
        models.storage.delete(self)
