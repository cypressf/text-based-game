from game import *
from game_runner import Runner

if __name__ == "__main__":
    r = Runner()
    w = r.world
    olin = Location("Olin", "A cool school.")
    needham = Location("Needham", "A cool town.")

    # link the two locations together
    olin.add_location(needham)
    needham.add_location(olin)

    # create the player
    cypress = Player("Cypress", "A cool guy.", location=olin)

    # create the items
    pen = Item("Pen", "A blue pen.", location=olin, is_movable=True)

    # add everything to the game world
    w.add_thing(cypress)
    w.add_thing(needham)
    w.add_thing(olin)
    w.add_thing(pen)
    r.run()