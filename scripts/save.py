import shelve
import main as game

d = shelve.open('data') # here you will save the score variable   
d['level'] = game.current_level        # thats all, now it is saved on disk.
d.close()
