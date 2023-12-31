#!/usr/bin/python3
"""test for db storage"""
import unittest
import pep8
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = DBStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass
        
    def test_pep8_DBStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in DB Storage"""
        storage = DBStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._DBStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = DBStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload(self):
        """Tests reload"""
        storage = DBStorage()
        storage.reload()
        self.assertIsNotNone(storage.all())
        self.assertEqual(type(storage.all()), dict)
        self.assertIs(storage._DBStorage__objects, storage.all())

    def test_delete(self):
        """Tests delete"""
        storage = DBStorage()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        storage.save()
        storage.delete(user)
        self.assertNotIn(user, storage.all().values())

    def test_get(self):
        """Tests get"""
        storage = DBStorage()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        storage.save()
        self.assertEqual(storage.get("User", 123455), user)

    def test_count(self):
        """Tests count"""
        storage = DBStorage()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        storage.save()
        self.assertEqual(storage.count("User"), 1)
        self.assertEqual(storage.count(), 1)

if __name__ == "__main__":
    unittest.main()
