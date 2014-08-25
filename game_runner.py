#!/usr/bin/python

from game import *
runner = Runner()
runner.load()
world = runner.world
player = world.get_player()

while True:
    # check the events and execute them until
    # there are no more to execute, then break
    while True:
        event_text = world.load_events()
        if event_text:
            for page in event_text:
                print page
                command = raw_input("press enter to continue")
        else:
            break
    
    command = raw_input("> ")
    command = command.split()
    verb = command[0].lower()
    if verb == "move":
        print("move not implemented")

    elif verb == "drop":
        #todo
        print("drop not implemented")

    elif verb == "pickup":
        print("pickup not implemented")

    elif verb == "look" or verb == "examine":
        print("look not implemented")

    elif verb == "go" or verb == "goto":
        if len(command) < 2:
            print("You wander aimlessly around, going nowhere in particular")
        else:
            location_name = command[1]
            location = world.get_location(location_name)
            if location is not None and player.move(location):
                print("You moved to {}".format(location.name))
                print(location.description)
            else:
                print("cannot move to {}".format(location_name))

    elif verb == "talk":
        print("talk not implemented")

    elif verb == "save":
        runner.save()

    elif verb == "quit":
        runner.save()
        break