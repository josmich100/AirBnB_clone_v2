#!/usr/bin/python3
"""
This module handles file storage functions
"""


import json
import importlib


class FileStorage:
    """
    This class handles serialization and deserialization of objects
        to/from a JSON file.
    """

    __file_path = "file.json"
    __objects = {}

    def classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def all(self):
        """Returns the dictionary of all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds an object to the internal dictionary.

        Args:
            obj: The object to add.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes and saves the dictionary of objects to a JSON file."""
        data = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(data, file)

    def reload(self):
        """Deserializes and loads objects from the JSON file."""
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
            for key, obj in data.items():
                self.__objects[key] = self.classes()[obj["__class__"]](**obj)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        key = "{}.{}".format(type(obj).__name__, obj.id) if obj else None
        # Use dict.pop method to safely remove the key
        self.__objects.pop(key, None)

    def close(self):
        """Call the reload method."""
        self.reload()
