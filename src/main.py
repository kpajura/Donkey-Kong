import pyxel
from constants import *
from Game import Game

def main():
    #Create the game window
    pyxel.init(WIDTH, HEIGHT, caption=CAPTION)
    #Load the pyxres file
    pyxel.load("../assets/my_resource.pyxres")

    pyxel.run(update, draw)
    
    
def update():
    if pyxel.btnp(pyxel.KEY_ESCAPE):                                        #Esc to quit game
        pyxel.quit()
        
        
    if pyxel.btn(pyxel.KEY_SPACE):
        Game()
    
    
    
    
    
def draw():
    pyxel.blt(45, 100, 1, 1, 0, 110, 28)
    text="Enter 'SPACE' to start the game!"
    pyxel.text(35, 150, text, 2)



#Game()


main()