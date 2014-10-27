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
        string += "Player ---- {}\n".format(str(self.player))
        for location in self.locations:
            string += "Location ---- {}\n".format(str(location))
        for item in self.items:
            string += "Items ---- {}\n".format(str(item))
        for event in self.events:
            string += "Event ---- {}\n".format(str(event))
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
            if item_name.lower() == item.name.lower():
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
            self.items.append(thing)
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
        self.location.add_item(self)

    def move(self, destination):
        """Sets the new location of the item to be 'destination'."""
        if not self.is_movable:
            return False
        else:
            if self.location is not None:
                self.location.remove_item(self)
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
        if locations is None:
            locations = []
        if items is None:
            items = []
        self.locations = locations
        self.items = items

    def add_item(self, item):
        self.items.append(item)

    def add_location(self, location):
        self.locations.append(location)

    def remove_location(self, location):
        self.locations.remove(location)

    def remove_item(self, item):
        self.items.remove(item)


class Player(Thing):
    """Represents a player in the game."""

    def __init__(self, name, desc, location=None, items=None):
        Thing.__init__(self, name, desc)
        if items is None:
            items = []
        self.location = location
        self.items = items
        self.observed_things = []

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
        self.observed_things.append(thing)

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
            if isinstance(var, list):
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
            if isinstance(vars(obj)[var_name], list):
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
        self.questions = []

    def __str__(self):
        return self.text

    def add_question(self, question):
        self.questions.append(question)

    def remove_question(self, question):
        self.questions.remove(question)


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
        self.questions = []

    def __str__(self):
        string = ""
        i = 1
        for question in self.questions:
            string = string + str(i) + ") " + str(question) + "\n"
            i += 1
        return string

    def add_question(self, question):
        self.questions.append(question)

    def ask(self, index):
        question = self.questions[index - 1]
        question.is_used = True
        return question.answer
