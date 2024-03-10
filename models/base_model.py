#!/usr/bin/python3
""" 
base_model.py defines all common 
attributes/methods for other classes
"""
import uuid
from datetime import datetime
from models import storage

class BaseModel():
    """Base model class"""
    def __init__(self, *args, **kwargs):
        """ instanciate class"""
        if len(kwargs) != 0:
            self.id = kwargs['id']
            self.created_at = datetime.fromisoformat(kwargs['created_at'])
            self.updated_at = datetime.fromisoformat(kwargs['updated_at'])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
    
    def __str__(self):
        """
        should return 
        [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """
        updates the public instance attribute updated_at 
        with the current datetime
        """
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        """
        returns a copy of a custom dictionary containing all 
        keys/values of __dict__ of the instance + class name
        This method will be the first piece of the serialization/deserialization process:
        create a dictionary representation with “simple object type” of our BaseModel
        """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
