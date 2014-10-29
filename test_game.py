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

    # create an npc
    npc = Person("James", "A random dude", location=olin)
    npc.conversation = Conversation()
    question = Question("What are you up to?")
    question.answer = Answer("Not much")
    npc.conversation.add_question(question)

    # create the events
    def pickup_pen_results():
        pen.description = "is it... dripping blood?"
    pickup_pen_event = Event("The world begins to tremble. You wonder if it was wise to take that pen.")
    pickup_pen_event.conditional = lambda: pen in cypress.items
    pickup_pen_event.actions = pickup_pen_results

    def draw_results():
        cypress.location = alien_world
    draw_event = Event("You scratch out some symbols on the paper. You are transported to a new dimension.")
    draw_event.conditional = lambda: pen in cypress.items_being_used and paper in cypress.items_being_used
    draw_event.actions = draw_results

    # add everything to the game world
    w.add_thing(cypress)
    w.add_thing(needham)
    w.add_thing(olin)
    w.add_thing(pen)
    w.add_thing(paper)
    w.add_thing(npc)
    w.events.append(pickup_pen_event)
    w.events.append(draw_event)
    r.run()