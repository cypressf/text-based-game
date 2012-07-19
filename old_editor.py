import pickle
from game import *
import os
import string


class Editor:
    """Holds all the things in the game together"""
    
    def __init__(self):
        self.world = World()
    
    def addThing(self, type):
        name = raw_input("Name: ")
        description = raw_input("Description: ")
        thing = type(name, description)
        self.world.addThing(thing)
        return thing
    
    def addEvent(self):
        e = Event()
        menu = ["Add trigger", "Add action", "Add text", "Done"]
        i = 1
        for item in menu:
            print str(i) + ". " + item
        choice = raw_input(": ")
        if choice == "1":
            objs = [self.world.group] + [self.world.things] + [self.world.events]
            i = 1
            print str(i) + "---> " + "Group"
            i = i + 1
            print "Events:"
            for thing in self.world.things:
                print str(i) + "---> " + thing
                i = i + 1
            print "Things:"
            for event in self.world.events:
                print str(i) + "---> " +  event
                i = i + 1
            obj_number = raw_input("chose an object: ")
            obj = objs[obj_number - 1]
            var = raw_input("type a variable: ")
            state_number = raw_input("chose a trigger state: ")
            if state_number == "string":
                state = raw_input("type a string: ")
            else:
                state = objs(state_number)
            
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
        
    def addPlayer(self):
        player = self.addThing(Player)
        print "Player " + player.name + " was created!"
    
    def addItem(self):
        item = self.addThing(Item)
        print "Item " + item.name + " was created!"
    
    def addLocation(self):
        location = self.addThing(Location)
        print "Location " + location.name + " was created!"        


filename = raw_input("enter a filename: ")
fpath = "./"+filename

if os.path.exists(fpath):
    print "File "+filename+" exists. Attempting to load game from "+fpath
    f = open(fpath, 'r')
    w = pickle.load(f)
    print "World " + str(w) + " was loaded successfully"
    
else:
    print "File "+filename+" will be created for a new "
    w = World()

def save():
    f = open(fpath, 'w')
    print "File was created at "+fpath
    pickle.dump(w, f)
    print str(w) + " has been saved to " + fpath
    

while True:
    
    print """    1. add a player
    2. add a location
    3. add an item
    4. save
    5. quit
    6. display object info
    7. edit locations
    8. edit player
    9. edit items"""
    
    choice = raw_input("What would you like to do? (enter a number): ")
    if choice == "1":
        w.addPlayer()
    elif choice == "2":
        w.addLocation()
    elif choice == "3":
        w.addItem()
    elif choice == "4":
        save()
    elif choice == "5":
        while True:
            s = raw_input("Would you like to save first? (y/n): ")
            if s.lower() in ["yes", "y", "yep"]:
                save()
                exit()
            elif s.lower() in ["n", "no", "nope", "naw", "naw bra"]:
                exit()
            else: print "Please type 'yes' or 'no'"
    elif choice == "6":
        print str(w)
        print w.player
        for item in w.items: print item
        for location in w.locations: print location
    elif choice == "7":
        print """   a. edit name
    
        """
        
    else:
        print "that's not a valid menu item"