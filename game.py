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
    # I think it's always executing it, or something weird because 'if event.__check()'
    # is not the same as 'bool = event.__check(), if bool'
    def load_events(self):
        """Checks all events in self.events and executes them if they are triggered."""
        return [event for event in self.events if event._Event__check()]

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
        # TODO: actually put the items in "use" state.
        # TODO: It could be helpful to construct a list of "currently used" items
        # TODO: that the event loop could look at.
        return things


class Event:
    """
    Represents an event in the game
    
    An event has two callbacks: conditional(), which tells
    it whether or not to trigger the actions; and and actions(),
    which tell it how to change the game state when it triggers.

    An event also has text. This can be either a list of pages
    of text, or simply a single block of text.
    """

    def __init__(self, text, conditional=None, actions=None):
        self.conditional = conditional  # a function that tests to see if this event has triggered yet
        self.actions = actions  # a function that changes the state fo the world when this event triggers
        self.is_used = False  # to prevent multiple executions
        self.text = text  # [page1, page2, page3... ] what it tells the player as the event is happening

    def __str__(self):
        string = ""
        if self.text is None:
            string += "No text"
        else:
            string += "\nText:\n"
            if isinstance(self.text, basestring):
                string += self.text + "\n"
            else:
                for page in self.text:
                    string += page + "\n-----------------\n"
        return string

    def __check(self):
        return not self.is_used and self.conditional()

    def __execute(self):
        if self.is_used:
            return False
        self.actions()
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
