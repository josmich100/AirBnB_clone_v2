#!/usr/bin/python3
"""This is the console for AirBnB"""
import cmd
import re
from models import storage
from shlex import split

class HBNBCommand(cmd.Cmd):
    """This class is the entry point of the command interpreter."""
    prompt = "(hbnb) "
    all_classes = {"BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"}

    def emptyline(self):
        """Ignores empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Quit command to exit the program at the end of the file."""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it.

        Raises:
            SyntaxError: when there are no arguments given.
            NameError: when the object doesn't exist.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            obj = eval("{}()".format(my_list[0]))
            for pair in my_list[1:]:
                pair = pair.split('=', 1)
                if len(pair) == 1 or "" in pair:
                    continue
                match = re.search('^"(.*)"$', pair[1])
                cast = str
                if match:
                    value = match.group(1)
                    value = value.replace('_', ' ')
                    value = re.sub(r'(?<!\\)"', r'\\"', value)
                else:
                    value = pair[1]
                    cast = float if "." in value else int
                try:
                    value = cast(value)
                except ValueError:
                    pass
                setattr(obj, pair[0], value)
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance.

        Raises:
            SyntaxError: when there are no arguments given.
            NameError: when the object doesn't exist.
            IndexError: when there is no id given.
            KeyError: when there is no valid id given.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            print(objects.get(key, "** no instance found **"))
        except (SyntaxError, NameError, IndexError, KeyError):
            print("** invalid command **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.

        Raises:
            SyntaxError: when there are no arguments given.
            NameError: when the object doesn't exist.
            IndexError: when there is no id given.
            KeyError: when there is no valid id given.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            objects.pop(key, None)
            storage.save()
        except (SyntaxError, NameError, IndexError, KeyError):
            print("** invalid command **")

    def do_all(self, line):
        """Prints all string representation of all instances.

        Raises:
            NameError: when the object doesn't exist.
        """
        objects = storage.all()
        my_list = []
        if not line:
            my_list = list(objects.values())
        else:
            try:
                args = line.split(" ")
                if args[0] not in self.all_classes:
                    raise NameError()
                my_list = [obj for key, obj in objects.items() if key.split('.')[0] == args[0]]
            except NameError:
                print("** class doesn't exist **")
                return
        print(my_list)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.

        Raises:
            SyntaxError: when there are no arguments given.
            NameError: when the object doesn't exist.
            IndexError: when there is no id given.
            KeyError: when there is no valid id given.
            AttributeError: when there is no attribute given.
            ValueError: when there is no value given.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            obj = objects[key]
            try:
                obj.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                obj.__dict__[my_list[2]] = my_list[3]
            storage.save()
        except (SyntaxError, NameError, IndexError, KeyError, AttributeError, ValueError):
            print("** invalid command **")

    def count(self, line):
        """Count the number of instances of a class."""
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.all_classes:
                raise NameError()
            count = sum(1 for key in storage.all() if key.split('.')[0] == my_list[0])
            print(count)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """Strip the argument and return a string of command.

        Args:
            args: input list of args.

        Returns:
            returns a string of arguments.
        """
        new_list = [args[0]]
        try:
            my_dict = eval(args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.extend([((new_str.split(", "))[0]).strip('"'), my_dict])
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(new_list)

    def default(self, line):
        """Retrieve all instances of a class and retrieve the number of instances."""
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(f'{key} "{k}" "{v}"')
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
