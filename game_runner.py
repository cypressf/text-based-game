#!/usr/bin/python

from game import *
import pickle
import os
import string
r = Runner()
r.load()

while True:
    
    # check the events and execute them until
    # there are no more to execute, then break
    while True:
        event_text = r.world.loadEvents()
        if event_text != False:
            for page in event_text:
                print page
                s = raw_input("press enter to continue")
        else break
    
    s = raw_input("> ")
    s = s.split()
    verb = s[0].lower()
    if verb == "move"
    if verb == "drop"
    if verb == "pickup"
    if verb == "look" or verb == "examine"
    if verb == "go" or verb == "goto"
    if verb == "talk"
    