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

    def load_events(self):
        """Checks all events in self.events and executes them if they are triggered."""
        return [event for event in self.events if event._Event__check()]

    def get_location(self, location_name):
        """Given the name of a location, return a matching Location, or None."""
        for location in self.locations:
            if location_name.lower() == location.name.lower():
                return location
        return None

    def get_item(self, item_name):
        """Given the name of an item, return a matching Item, or None."""
        for item in self.items:
            if item_name.lower() == item.name.lower():
                return item
        return None

    def get_person(self, person_name):
        """Given the name of a person, return the matching Person, or None."""
        for person in self.characters:
            if person_name.lower() == person.name.lower():
                return person
        return None

    def add_thing(self, thing):
        """Add a person, location, item, or player to the game world."""
        if isinstance(thing, Person):
            self.characters.append(thing)
        elif isinstance(thing, Location):
            self.locations.append(thing)
        elif isinstance(thing, Item):
            self.items.append(thing)
        elif isinstance(thing, Player):
            self.player = thing

    def add_things(self, things):
        """
        Add a list of things to the game world. Convenience method to avoid calling add_thing many times.
        """
        for thing in things:
            self.add_thing(thing)


class Thing:
    """Building block for most objects in the game."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_hidden = False
        self.observed = 0

    def __str__(self):
        return self.name


class Item(Thing):
    """Represents all Items in the game."""

    def __init__(self, name, description, location, is_movable=False):
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
    """Represents a non-playable-character in the game.
    
    People are similar to Items, but they each
    have a conversation object in them as well.

    If you specify is_movable=True, you'll be able to pickup the person
    and put them in your inventory. I'm leaving this as an option in case
    your game contains an anthropomorphic map, a digital communicator,
    or a little fairy gnome or something that you can pick up.
    """

    def __init__(self, name, description, location=None, is_movable=False, conversation=None):
        Item.__init__(self, name, description, location, is_movable)
        self.conversation = conversation

    def __str__(self):
        return self.name


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
        self.items_being_used = []
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
        if self.can_see(thing):
            thing.observed += 1
            self.observed_things.append(thing)
            return True
        else:
            return False        

    def use(self, things):
        for thing in things:
            if not self.can_see(thing):
                return False
        self.items_being_used = things
        return self.items_being_used

    def can_see(self, thing):
        return thing in self.location.items + self.items + [self.location]


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
        return "    \"{}\"".format(self.text)

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
        self.text


class Conversation:
    def __init__(self):
        self.questions = []
        self.bye_message = "Bye!"

    def __str__(self):
        string = ""
        i = 1
        for question in self.questions:
            string += "{}) {}\n".format(i, question.text)
            i += 1
        return string

    def add_question(self, question):
        self.questions.append(question)

    def ask(self, index):
        question = self.questions[index - 1]
        question.is_used = True
        self.questions.remove(question)
        self.questions += question.answer.questions
        return question.answer
