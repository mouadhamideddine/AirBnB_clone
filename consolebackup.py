#!/usr/bin/python3
"""  command interpreter """
import cmd
from models import storage


class HBNBCommand(cmd.Cmd):
    """hbnb console"""
    prompt = "(hbnb) "
    classes = storage.my_classes

    def emptyline(self):
        """when empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_EOF(self, arg):
        """exit the program"""
        return True
    
    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file) 
        and prints the id. Ex: $ create BaseModel
        """
        if arg == '':
            print("** class name missing **")
            return
        if arg not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        arg_class = HBNBCommand.classes[arg]
        instance = arg_class()
        instance.save()
        print(instance.id)
    
    def do_show(self, arg):
        """
         Prints the string representation of an instance based on
        the class name and id. Ex: $ show BaseModel 1234-1234-1234.
        """
        if arg == '' or arg is None:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) != 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])
 
    
    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file)
        """
        if arg == '' or arg is None:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) != 2:
             print("** instance id missing **")
             return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del(storage.all()[key])
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances 
        based or not on the class name. Ex: $ all BaseModel or $ all
        """
        do_all_list = []
        if arg == '' or arg is None:
            for value in storage.all().values():
                do_all_list.append(value.__str__())
            print(do_all_list)
            return
        if arg not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        for value in storage.all().values():
            if isinstance(value, HBNBCommand.classes[arg]):
                do_all_list.append(value.__str__())
        print(do_all_list)
        return
    
    def do_update(self, arg):
        """
         Updates an instance based on the class name and id by adding or updating attribute 
         (save the change into the JSON file). Ex: $ update BaseModel 1234-1234-1234 email 
         "aibnb@mail.com"
        """
        args = arg.split()
        if len(args) == 0 or args is None:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        the_instance = storage.all()[key]
        type_cast = type(the_instance.to_dict()[args[2]])
        args_3 = type_cast(args[3])
        setattr(the_instance, args[2], args_3)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()