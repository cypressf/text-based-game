#!/usr/bin/python
from game import *


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

    def execute_events(self):
        """Check the events and execute them until there are no more to execute"""
        while True:
            triggered_events = self.world.load_events()
            if triggered_events:
                for event in triggered_events:
                    event._Event__execute()
                    if isinstance(event.text, basestring):
                        print event.text
                    else:
                        for page in event.text:
                            print page
                            raw_input("press enter to continue")
            else:
                self.world.player.items_being_used = []
                break

    def run(self):
        player = self.world.player
        while True:
            self.execute_events()

            command = raw_input("> ")
            command = command.split()
            if not command:
                continue
            verb = command[0].lower()
            if verb == "move":
                print("move not implemented")

            elif verb == "drop":
                if len(command) < 2:
                    print("You consider dropping something... no, never mind")
                else:
                    item_name = command[1]
                    item = self.world.get_item(item_name)
                    if player.drop_item(item):
                        print("You drop the {} to the ground.".format(item.name))
                    else:
                        print("You can't drop that.")

            elif verb == "pickup":
                if len(command) < 2:
                    print("You consider picking up something... no, never mind")
                else:
                    item_name = command[1]
                    item = self.world.get_item(item_name)
                    if item and player.pickup_item(item):
                        print("You pick up the {}".format(item.name))
                    else:
                        print("You can't pick that up")

            elif verb == "look" or verb == "examine":
                if len(command) < 2:
                    print("You look around you.")
                    print(player.location)
                    for item in player.location.items:
                        print(item)
                else:
                    item_name = command[1]
                    item = self.world.get_item(item_name)
                    if not item:
                        item = self.world.get_location(item_name)
                    if item and item in player.location.items + player.items + [player.location]:
                        player.observe(item)
                        print(item)
                    else:
                        print("You see no {0}. Where's the {0}?".format(item_name))

            elif verb == "go" or verb == "goto":
                if len(command) < 2:
                    print("You wander aimlessly around, going nowhere in particular")
                else:
                    location_name = command[1]
                    location = self.world.get_location(location_name)
                    if location is not None and player.move(location):
                        print("You moved to {}".format(location.name))
                        print(location.description)
                    else:
                        print("cannot move to {}".format(location_name))

            elif verb == "inventory":
                if not player.items:
                    print("You have nothing in your backpack.")
                else:
                    print("You peek inside your bottomless backpack. You have:")
                    for item in player.items:
                        print(item)

            elif verb == "use":
                if len(command) < 2:
                    print("You think about using something... then think again.")
                else:
                    items = []
                    for item_name in command[1:]:
                        if item_name in ["with", "and", "on"]:
                            continue
                        item = self.world.get_item(item_name)
                        if item:
                            items.append(item)
                    if items:
                        player.use(items)

            elif verb == "talk":
                if len(command) < 2:
                    print("You mutter to yourself, absentmindedly.")
                else:
                    for word in command[1:]:
                        if word in ["to", "with"]:
                            continue
                        else:
                            person = self.world.get_person(word)
                            break
                    if person and player.can_see(person):
                        while True:
                            if not person.conversation.questions:
                                print(person.conversation.bye_message)
                                break
                            print(person.conversation)
                            choice = raw_input("enter a number, or \"bye\" to leave: ")
                            if choice == "bye":
                                print(person.conversation.bye_message)
                                break
                            else:
                                print(person.conversation.ask(int(choice)))

            elif verb == "save":
                self.save()

            elif verb == "quit":
                self.save()
                break

if __name__ == "__main__":
    runner = Runner()
    runner.load()
    runner.run()
