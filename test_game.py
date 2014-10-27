from game import *
w = World()
p = Player("Cypress", "A cool guy.")
l = Location("Olin College", "A cool school.")
p.location = l
w.player = p
w.locations.append(l)
