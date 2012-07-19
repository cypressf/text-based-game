#!/usr/bin/python

from game import *
import pickle
import os
import string
e = Editor()
e.load()

while True:
    menu1 = ["events","items","people","locations","player", "quit"]
    i = 1
    for item in menu1:
        print str(i) + ") " + item
        i += 1
    
    choice = raw_input(": ")
    if choice == "1":
        while True:
            e.printEvents()
            s = raw_input(": ")
            if s == "main": break
            event = e.getEvent(int(s))
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
        
    elif choice  == "2":
        while True:
            e.printItems()
            s = raw_input(": ")
            if s == "main": break
            item = e.getItem(int(s))
            e.printItemDetail(int(s))
        
    elif choice == "3":
        while True:
            e.printPeople()
            s = raw_input(": ")
            if s == "main": break
            person = e.getPerson(int(s))
            e.getPersonDetail(int(s))
        
    elif choice == "4":
        while True:
            e.printLocations()
            s = raw_input(": ")
            if s == "main": break
            location = e.getLocation(int(s))
            e.printLocationDetail(int(s))
        
    elif choice == "5":
        e.printPlayerDetail()
        player = e.getPlayer()
        
    elif choice == "6":
        while True:
            s = raw_input("Would you like to save first? (y/n): ")
            if s.lower() in ["yes", "y", "yep"]:
                e.save()
                exit()
            elif s.lower() in ["n", "no", "nope", "naw", "naw bra"]:
                exit()
            else: print "Please type 'yes' or 'no'"
    else:
        print "Enter a number from 1 to 6"
        continue