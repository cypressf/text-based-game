from game import *
from game_runner import Runner

if __name__ == "__main__":
    r = Runner()
    w = r.world
    olin = Location("Olin", "This place looks quiet today. The road to Needham is calling to you. Maybe you should go there today...")
    needham = Location("Needham", "Ahhh. Needham. You've had enough already. Back to Olin?")
    alien_world = Location("????", "What is this place? How will you ever get home? The air is thick with an acrid smell.")

    # link the locations together
    olin.add_location(needham)
    needham.add_location(olin)

    # create the player
    cypress = Player("Cypress", "A cool guy.", location=olin)

    # create the items
    pen = Item("Pen", "A blue pen.", location=olin, is_movable=True)
    paper = Item("Paper", "A plain, white sheet of paper", location=olin, is_movable=True)

    # create an npc
    npc = Person("Ishmael", "This man looks like he's still getting accustomed to his land-legs", location=olin)
    npc.conversation = Conversation()
    question1 = Question("What are you up to?")
    answer = Answer("Not much")
    question1.answer = answer

    question2 = Question("Not very talkative, are you?")
    question2.answer = Answer("There is no folly of the beast of the earth\n "
                              "which is not infinitely outdone by the madness of men.")
    question3 = Question("You look sleepy. What's on your mind?")
    question3.answer = Answer("There are certain queer times and occasions in this strange mixed affair\n "
                              "we call life when a man takes this whole universe for avast practical joke,\n "
                              "though the wit thereof he but dimly discerns, and more than suspects that the\n "
                              "joke is at nobody's expense but his own.")
    answer.add_question(question2)
    answer.add_question(question3)
    npc.conversation.add_question(question1)

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
    w.add_things([cypress, needham, olin, pen, paper, npc])
    w.events += [pickup_pen_event, draw_event]
    r.run()