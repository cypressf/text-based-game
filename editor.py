#!/usr/bin/python

from game import *
editor = Editor()
editor.load()


def events_menu():
    while True:
        if not editor.print_events():
            break
        s = raw_input("enter event number, or \"main\" to go to main menu: ")
        if s == "main":
            break
        elif s.isdigit():
            event = editor.get_event(int(s))
            print event
            # todo create an event editor
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


def items_menu():
    while True:
        if not editor.print_items():
            break
        s = raw_input("enter item number, or \"main\" to go to main menu: ")
        if s == "main":
            break
        elif s.isdigit():
            item = editor.get_item(int(s))
            editor.print_item_detail(int(s))


def people_menu():
    while True:
        if not editor.print_people():
            break
        s = raw_input("enter person number, or \"main\" to go to main menu: ")
        if s == "main":
            break
        elif s.isdigit():
            person = editor.get_person(int(s))
            editor.print_person_detail(int(s))


def locations_menu():
    while True:
        if not editor.print_locations():
            break
        s = raw_input("enter location number, or \"main\" to go to main menu: ")
        if s == "main":
            break
        elif s.isdigit():
            location = editor.get_location(int(s))
            editor.print_location_detail(int(s))


def player_menu():
    editor.print_player_detail()
    player = editor.get_player()


def quit_menu():
    while True:
        s = raw_input("Would you like to save first? (y/n): ")
        if s.lower() in ["yes", "y", "yep"]:
            editor.save()
            exit()
        elif s.lower() in ["n", "no", "nope", "naw", "naw bra"]:
            exit()
        else:
            print "Please type 'yes' or 'no'"

while True:
    main_menu_order = ["events", "items", "people", "locations", "player", "quit"]
    main_menu = {
        "events": events_menu,
        "items": items_menu,
        "people": people_menu,
        "locations": locations_menu,
        "player": player_menu,
        "quit": quit_menu
    }

    for menu_name in main_menu_order:
        print("-> " + menu_name)

    choice = raw_input(": ")
    if choice in main_menu:
        main_menu[choice]()
    else:
        print "Select an item to edit"
        continue