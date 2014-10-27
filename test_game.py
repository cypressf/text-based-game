from game import *
from game_runner import Runner

if __name__ == "__main__":
    r = Runner()
    w = r.world
    olin = Location("Olin", "A cool school.")
    needham = Location("Needham", "A cool town.")
    alien_world = Location("????", "What is this place? The air is thick with an acrid smell.")

    # link the locations together
    olin.add_location(needham)
    needham.add_location(olin)

    # create the player
    cypress = Player("Cypress", "A cool guy.", location=olin)

    # create the items
    pen = Item("Pen", "A blue pen.", location=olin, is_movable=True)
    paper = Item("Paper", "A plain, white sheet of paper", location=olin, is_movable=True)

    # create the events
    pickup_pen_event = Event("The world begins to tremble. You wonder if it was wise to take that pen.")
    pickup_pen_event.conditional = lambda: pen in cypress.items

    def event_results():
        pen.description = "is it... dripping blood?"

    pickup_pen_event.actions = event_results

    draw_event = Event("You scratch out some symbols on the paper. You are automatically transported to a new dimension")

    # add everything to the game world
    w.add_thing(cypress)
    w.add_thing(needham)
    w.add_thing(olin)
    w.add_thing(pen)
    w.events.append(pickup_pen_event)
    r.run()