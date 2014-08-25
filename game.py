# todo: figure out where 'load' and 'save' should be.
# methods of Runner and Editor? functions of the game package?
# methods of World?


class Runner:
    def __init__(self):
        self.world = World()

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

        filename = raw_input("Enter a name for your saved game: ")
        file_path = "./" + filename
        f = open(file_path, 'w')
        pickle.dump(self.world, f)
        f.close()
        print "The game has been saved to " + filename


class Editor:
    """Used to easily manipulate objects in a World (stored in self.world)"""

    def __init__(self, ):
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


class World:
    """Contains all the objects in the game
    
    World has two lists: events and things. Things are all Locations, People, and Items.
    World can easily be pickled and saved so the objects can be accessed later.
    """

    def __init__(self, player=None, locations=None, items=None, events=None, characters=None):
        if locations is None:
            locations = []
        if items is None:
            items = []
        if events is None:
            events = []
        if characters is None:
            characters = []

        self.locations = locations
        self.player = player
        self.items = items
        self.events = events
        self.characters = characters
        self.group = None

    def __str__(self):
        string = "\n"
        string += format("Player ---- {}\n", str(self.player))
        for location in self.locations:
            string += format("Location ---- {}\n", str(location))
        for item in self.items:
            string += format("Items ---- {}\n", str(item))
        for event in self.events:
            string += format("Event ---- {}\n", str(event))
        return string

    # todo
    # test loadEvents to make sure it executes event only when check() returns true
    # I think it's always executing it, or something weird because 'if event.check()'
    # is not the same as 'bool = event.check(), if bool'
    def load_events(self):
        """Checks all events in self.events and executes them if they are triggered."""
        for event in self.events:
            if event.check():
                event.execute()
                return event.text
        return False

    def get_location(self, location_name):
        for location in self.locations:
            if location_name.lower() == location.name.lower():
                return location
        return None

    def get_item(self, item_name):
        for item in self.items:
            if item_name == item.name:
                return item
        return None

    def get_things(self, thing_class):
        things = []
        if thing_class is Item:
            things = self.items
        elif thing_class is Person:
            things = self.characters
        elif thing_class is Location:
            things = self.locations
        elif thing_class is Player:
            things = [self.player]
        return things

    def add_thing(self, thing):
        if isinstance(thing, Person):
            self.characters.append(thing)
        elif isinstance(thing, Location):
            self.locations.append(thing)
        elif isinstance(thing, Item):
            self.items(thing)
        elif isinstance(thing, Player):
            self.player = thing


class Thing:
    """Building block for most objects in the game."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_hidden = False
        self.observed = 0

    def __str__(self):
        return self.name + ": " + self.description


class Item(Thing):
    """Represents all Items in the game."""

    def __init__(self, name, description, location=None, is_movable=False):
        """Creates an Item.
        
        Just like a Thing, an item only requires a name and a description,
        but a location, linked items, and an "is movable" boolean can be
        added.
        
        """
        Thing.__init__(self, name, description)
        self.is_movable = is_movable
        self.location = location

    def move(self, destination):
        """Sets the new location of the item to be 'destination'."""
        if not self.is_movable:
            return False
        else:
            if self.location is not None:
                self.location.removeItem(self)
            self.location = destination
            destination.add_item(self)
            return True


class Person(Item):
    """Represents all People in the game.
    
    People are similar to Items, but they each
    have a conversation object in them as well
    """

    def __init__(self, name, description, location=None, is_movable=False, conversation=None):
        Item.__init__(self, name, description, location, is_movable)
        self.conversation = conversation

    def __str__(self):
        return self.name + ": " + self.description + "\n" + str(self.conversation)


class Location(Thing):
    """Represents all locations in the game
    
    Like a Thing, a Location only requires a name and a description, but
    you can also add linked locations, and linked items.
    
    The 'locations' variable holds all the linked locations.
    The 'items' variable holds all the linked items.
    
    To add a location, use self.locations.append(location)
    To remove a location use self.locations.remove(location)
    
    To add an item, use self.items.append(item)
    To remove an item, use self.items.remove(item)
    """

    def __init__(self, name, description, locations=None, items=None):
        Thing.__init__(self, name, description)
        self.locations = locations
        self.items = items

    def add_item(self, item):
        if self.items is None:
            self.items = [item]
        else:
            self.items.append(item)

    def add_location(self, location):
        if self.locations is None:
            self.locations = [location]
        else:
            self.locations.append(location)

    def remove_location(self, location):
        self.locations.remove(location)

    def remove_item(self, item):
        self.items.remove(item)


class Player(Thing):
    """Represents a player in the game."""

    def __init__(self, na, desc, location=None, items=None):
        Thing.__init__(self, na, desc)
        if items is None:
            items = []
        self.location = location
        self.items = items
        self.observed_things = None

    def can_move(self, location):
        if self.location is None:
            return False
        if self.location.locations is None:
            return False
        return location in self.location.locations

    def move(self, location):
        if self.can_move(location):
            self.location = location
            return True
        else:
            return False

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        """Player gets rid of item, placing it in the current location.
        
        Don't do anything if the player is not in a location or doesn't
        have the specified item
        """

        if item not in self.items or self.location is None:
            return False

        else:
            return item.move(self.location)

    def pickup_item(self, item):
        """Player picks up item from current location."""
        if item not in self.location.items:
            return False
        else:
            item.move(self)
            return True

    def observe(self, thing):

        thing.observed += 1
        if self.observed_things is None:
            self.observed_things = [thing]
        else:
            self.observed_things.append(thing)
        return True

    def use(self, things):
        usable_things = self.location.items + self.items + [self.location]
        for thing in things:
            if thing not in usable_things:
                return False
        return things


class Event:
    """Represents all events in the game
    
    An event has triggers, which tell it when
    to execute; and actions, which tell it what to
    do. All triggers are in the form of states:
    it checks the state of specific objects to see
    if they match the trigger state. All actions
    are in the form of object-state modification
    lists.
    """

    def __init__(self):
        self.triggers = None  # [{"object": object, "variable_name": variable_name, "state":state}, ...]
        self.actions = None  # [{"object": object, "variable_name": variable_name, "state":state}, ...]
        self.is_used = False  # to prevent multiple executions
        self.text = None  # [page1, page2, page3... ] what it tells the player as the event is happening
        self.location = None

    def __str__(self):
        if self.triggers is None:
            string = "No triggers\n"
        else:
            string = "Triggers:\n"
            for trigger in self.triggers:
                obj = trigger["object"]
                var = trigger["variable_name"]
                trigger_state = trigger["state"]
                current_state = vars(obj)[var]
                if current_state == trigger_state:
                    string += "* "
                string = string + var + " of " + repr(obj) + ": current state " + str(
                    current_state) + ", trigger state " + str(trigger_state) + "\n"

        if self.actions is None:
            string += "No actions\n"
        else:
            string += "\nActions:\n"
            for action in self.actions:
                obj = action["object"]
                var = action["variable_name"]
                new_state = action["state"]
                current_state = vars(obj)[var]
                string = string + var + " of " + repr(obj) + ": current state " + str(
                    current_state) + ", new state " + str(new_state) + "\n"

        if self.text is None:
            string += "No text"
        else:
            string += "\nText:\n"
            for page in self.text:
                string = string + page + "\n-----------------\n"
        return string

    def add_trigger(self, obj, variable, value, opposite=False):
        if self.triggers is None:
            self.triggers = [{"object": obj, "variable_name": variable, "state": value, "opposite": opposite}]
        else:
            self.triggers.append({"object": obj, "variable_name": variable, "state": value, "opposite": opposite})

    def add_action(self, obj, variable, value):
        if self.actions is None:
            self.actions = [{"object": obj, "variable_name": variable, "state": value}]
        else:
            self.actions.append({"object": obj, "variable_name": variable, "state": value})

    def add_text(self, text):
        if self.text is None:
            self.text = [text]
        else:
            self.text.append(text)

    def check(self):
        if self.is_used:
            return False
        if self.triggers is None:
            return True
        for trigger in self.triggers:
            obj = trigger["object"]
            state = trigger["state"]
            var_name = trigger["variable_name"]
            var = vars(obj)[var_name]
            if var.__class__.__name__ == "List":
                if trigger["opposite"]:
                    if len(var) != len(state):
                        return True
                    for item in var:
                        if item not in state:
                            return True
                    return False

                else:
                    if len(var) != len(state):
                        return False
                    for item in var:
                        if item not in state:
                            return False
                    return True
            else:
                if trigger["opposite"]:
                    if var == state:
                        return False
                else:
                    if var != state:
                        return False
        return True

    def execute(self, append=True):
        if self.is_used:
            return False
        for action in self.actions:
            obj = action["object"]
            state = action["state"]
            var_name = action["variable_name"]
            if vars(obj)[var_name].__class__.__name__ == "List":
                if append:
                    vars(obj)[var_name] = vars(obj)[var_name] + state
                else:
                    vars(obj)[var_name] = state
            else:
                vars(obj)[var_name] = state
        self.is_used = True
        return True


class Answer:
    def __init__(self, text):
        self.text = text
        self.questions = None

    def __str__(self):
        return self.text

    def add_question(self, question):
        if self.questions is None:
            self.questions = [question]
        else:
            self.questions.append(question)

    def remove_question(self, question):
        if self.questions is None:
            return False
        for q in self.questions:
            if q is question:
                self.questions.remove(question)
                return True
        return False


class Question:
    def __init__(self, text):
        self.text = text
        self.answer = None
        self.is_used = False

    def __str__(self):
        if self.is_used:
            return "Re-ask:", self.text
        else:
            return "Ask:", self.text


class Conversation:
    def __init__(self):
        self.questions = None

    def __str__(self):
        string = ""
        i = 1
        for question in self.questions:
            string = string + str(i) + ") " + str(question) + "\n"
            i += 1
        return string

    def add_question(self, question):
        if self.questions is None:
            self.questions = [question]
        else:
            self.questions.append(question)

    def ask(self, index):
        q = self.questions[index - 1]
        q.is_used = True
        return q.answer