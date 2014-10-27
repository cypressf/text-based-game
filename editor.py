#!/usr/bin/python
from game import *


class Editor:
    """Used to easily manipulate objects in a World (stored in self.world)"""

    def __init__(self):
        self.world = World()

    def start(self):
        self.load()
        while True:
            main_menu_order = ["events", "items", "people", "locations", "player", "quit"]
            main_menu = {
                "events": self.events_menu,
                "items": self.items_menu,
                "people": self.people_menu,
                "locations": self.locations_menu,
                "player": self.player_menu,
                "quit": self.quit_menu
            }

            for menu_name in main_menu_order:
                print("-> " + menu_name)

            choice = raw_input(": ")
            if choice in main_menu:
                main_menu[choice]()
            else:
                print "Select an item to edit"
                continue

    def events_menu(self):
        while True:
            if not self.print_things(self.world.events):
                break
            s = raw_input("enter event number, or \"main\" to go to main menu: ")
            if s == "main":
                break
            elif s.isdigit():
                # todo edit the event
                event = self.world.events[int(s) - 1]
                # while True:
                #                 cmd = raw_input("type 'add' or 'remove' followed by 'trigger' or 'action'")
                #                 cmd = cmd.split()
                #                 if cmd[0].lower() == "add":
                #                     if cmd[1].lower() == "action":
                #                     if cmd[1].lower() == "trigger":
                #                 elif cmd[0].lower() == "remove":
                #                     if cmd[1].lower() == "action":
                #                     if cmd[1].lower() == "trigger":
                #                 else: continue

    def items_menu(self):
        while True:
            if not self.print_things(self.world.items):
                break
            s = raw_input("enter item number, or \"main\" to go to main menu: ")
            if s == "main":
                break
            elif s.isdigit():
                # todo: edit the item
                item = self.world.items[int(s) - 1]
                self.print_thing_details(item)

    def people_menu(self):
        while True:
            if not self.print_things(self.world.characters):
                break
            s = raw_input("enter person number, or \"main\" to go to main menu: ")
            if s == "main":
                break
            elif s.isdigit():
                # todo: edit the person
                person = self.world.characters[int(s) - 1]
                self.print_thing_details(person)

    def locations_menu(self):
        while True:
            if not self.print_things(self.world.characters):
                break
            s = raw_input("enter location number, or \"main\" to go to main menu: ")
            if s == "main":
                break
            elif s.isdigit():
                # todo: edit the location
                location = self.world.locations[int(s) - 1]
                self.print_thing_details(location)

    def player_menu(self):
        self.print_thing_details(self.world.player)
        # todo: edit the player

    def quit_menu(self):
        while True:
            s = raw_input("Would you like to save first? (y/n): ")
            if s.lower() in ["yes", "y", "yep"]:
                self.save()
                exit()
            elif s.lower() in ["n", "no", "nope", "naw", "naw bra"]:
                exit()
            else:
                print "Please type 'yes' or 'no'"

    def __addThing__(self, thing_class):
        """Adds Thing of class 'type' to editor's World.

        Do not use this method directly; instead, use add_item, add_location,
        add_player, or add_person.
        """
        name = raw_input("Name: ")
        description = raw_input("Description: ")

        # thing_class is a reference to the class of object that you are creating
        thing = thing_class(name, description)
        self.world.add_thing(thing)

        return thing

    def add_player(self):
        """Adds a Player to the editor's World"""
        player = self.__addThing__(Player)
        print "Player " + player.name + " was created!"

    def add_item(self):
        """Adds an Item to the editor's World"""
        item = self.__addThing__(Item)
        print "Item " + item.name + " was created!"

    def add_location(self):
        """Adds a Location to the editor's World"""
        location = self.__addThing__(Location)
        print "Location " + location.name + " was created!"

    # todo
    # finish the addEvent method
    def add_event(self):
        """Adds an Event to the editor's World"""
        event = Event()
        self.world.add_event(event)
        return event
        # e = Event()
        # menu = ["Add trigger", "Add action", "Add text", "Done"]
        # i = 1
        # for item in menu:
        # print str(i) + ". " + item
        # choice = raw_input(": ")
        # if choice == "1":
        # objs = [self.world.group] + [self.world.things] + [self.world.events]
        # i = 1
        # print str(i) + "---> " + "Group"
        # i = i + 1
        # print "Events:"
        # for thing in self.world.things:
        # print str(i) + "---> " + thing
        # i = i + 1
        #     print "Things:"
        #     for event in self.world.events:
        #         print str(i) + "---> " +  event
        #         i = i + 1
        #     obj_number = raw_input("chose an object: ")
        #     obj = objs[obj_number - 1]
        #     var = raw_input("type a variable: ")
        #     state_number = raw_input("chose a trigger state: ")
        #     if state_number == "string":
        #         state = raw_input("type a string: ")
        #     else:
        #         state = objs(state_number)
        #
        # if choice == "2":
        #
        # if choice == "3":
        # if choice == "4":
        # triggers = [{"object": object, "variable_name": variable_name, "state":state}, ...]
        # actions = [{"object": object, "variable_name": variable_name, "state":state}, ...]
        # text = [page1, page2, page3... ] what it tells the player as the event is happening
        #  = raw_input(": ")
        # description = raw_input("Description: ")
        # thing = type(name, description)
        # self.world.addThing(thing)
        # return thing

    def print_things(self, things):
        """Prints the things passed to it."""
        i = 0
        if len(things) == 0:
            print("There are none of those")
            return False
        else:
            for thing in things:
                i += 1
                print str(i) + ")", thing
            return True

    def print_thing_details(self, thing):
        variables = vars(thing)
        for index in variables:
            print index + ": " + repr(variables[index])

    def load(self):
        """Loads a World from a pickled file and places it in Editor's World"""
        # change add to top
        import pickle
        import os

        filename = raw_input("enter a filename: ")
        file_path = "./" + filename

        if os.path.exists(file_path):
            print "File " + filename + " exists. Attempting to load game from " + filename
            f = open(file_path, 'r')
            self.world = pickle.load(f)
            f.close()
            print "Load complete"
            return self.world
        else:
            return False

    def save(self):
        """Saves a World from Editor's World to a pickled file"""
        # change add imports to top
        import pickle

        filename = raw_input("enter a filename: ")
        file_path = "./" + filename
        f = open(file_path, 'w')
        pickle.dump(self.world, f)
        f.close()
        print "The world has been saved to " + filename


if __name__ == "__main__":
    editor = Editor()
    editor.start()