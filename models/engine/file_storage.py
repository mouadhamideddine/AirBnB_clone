#!/usr/bin/python3
"""
FileStorage that serializes instances to a
JSON file and deserializes JSON file to instance
"""
import json
import os

class FileStorage():
    """
    FileStorage Class
    """
    __file_path = "file.json"
    __objects = {}
    my_classes = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def add_class(self):
         """store classes  in a dictionary to avoid import"""
         from models.base_model import BaseModel
         from models.user import User
         from models.state import State
         from models.review import Review
         from models.place import Place
         from models.city import City
         from models.amenity import Amenity
         FileStorage.my_classes = {
             'BaseModel' : BaseModel,
             'User' : User,
             'State' : State,
             'Review' : Review,
             'Place' : Place,
             'City' : City,
             'Amenity' : Amenity
             }

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        # comes out the issue to create a whole dictionary
        # then dump it or dump dictionary by dictionary
        # then i choose to give __str__ instead
        # then when i write a string it's loaded as a string again
        # coming back to dictionary
        # key in FileStorage.__objects.items() BaseModel.212803a4-3264-4eb5-a34d-f160866c6110
        # coming back to dictionary question
        # convert dictionary and put it all at once
        # AttributeError: 'dict' object has no attribute 'to_dict'
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as file:
            storage_dic = {}
            for key, value in FileStorage.__objects.items():
                 storage_dic[key] = value.to_dict()
            json.dump(storage_dic, file)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file (__file_path) exists;
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised)
        """
        # AttributeError: 'str' object has no attribute 'read'
        # was giving a file_path instead of file
        # problem not loading anything hence rewriting file and removing past data
        # for key, value in FileStorage.__objects.items(): removed to see interaction
        # thinking problem might be in the saving of json file
        # AttributeError: 'dict' object has no attribute 'to_dict' coming from save\
        # but i think it's not a problem in save i think the way json gets loaded because \
        # it's storing properly
        # i think i should convert the objects i load according to their dictionary
        # created reload_dic for that
        # i presume reload_dic is a double dictionary with classname id as key and dictionary \
        # of attributes
        # circular import problem BaseModel(value) from models.base_model import BaseModel
        # thought about adding a method to my class to store appropriate classes
        # using a metaclass might open a can of worms
        # try it dynamicaly
        # can't dynamicaly since necessarly i only the class name as a string not a pointer\
        # to it
        # import when you need worked
        self.add_class()
        reload_dic = {}
        if os.path.exists(FileStorage.__file_path) and os.path.getsize(FileStorage.__file_path) > 0:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                    reload_dic = json.load(file)
            # print("reload_dic",reload_dic)
            for key, value in reload_dic.items():
                if value['__class__'] in FileStorage.my_classes.keys():
                    the_class = FileStorage.my_classes[value['__class__']]
                    # print("the_class", the_class) the classs is right
                else:
                    return
                # print("value", value) #dictionary complete here
                # print("self.__objects",self.__objects) #self.__objects {}
                # print("key", key) #key User.f8108f48-9d43-4b1e-8500-1cf837ad2fab
                # print("the_class", the_class) right class
                # print("value", value) valid dictionary
                # print("value['email']", value['email']) key can be accessed here
                self.__objects[key] = the_class(**value)

        else:
            return