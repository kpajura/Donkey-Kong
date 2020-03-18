import pyxel
from random import randint
from constants import *
from Objects import *

class Game:

    def __init__(self):
        """
        Class constructor
        Creates all game's objects except for barrels
        """
        #Create the game window
        #pyxel.init(WIDTH, HEIGHT, caption=CAPTION)
        #Load the pyxres file
        #pyxel.load("../assets/my_resource.pyxres")

        #Lists for platforms, ladders and barrels
        self.__platforms = []
        self.__ladders = []
        self.__barrels = []

        #First platform
        self.__platforms.append(Platform(5,245,27))
        #Middle platforms
        for i in range(5):
            self.__platforms.append(Platform((i%2)*21+5, 214-i*31, 24))
        #Last platform
        self.__platforms.append(Platform(90, 59, 6))

        #Ladders
        self.__ladders.append(Ladder(85, 239, True))
        self.__ladders.append(Ladder(150, 239, False))
        self.__ladders.append(Ladder(45, 208, False))
        self.__ladders.append(Ladder(120, 208, False))
        self.__ladders.append(Ladder(68, 177, True))
        self.__ladders.append(Ladder(100, 177, False))
        self.__ladders.append(Ladder(160, 177, False))
        self.__ladders.append(Ladder(30, 146, False))
        self.__ladders.append(Ladder(75, 146, False))
        self.__ladders.append(Ladder(127, 146, True))
        self.__ladders.append(Ladder(90, 115, True))
        self.__ladders.append(Ladder(140, 115, False))
        self.__ladders.append(Ladder(122, 84, False))
        self.__ladders.append(Ladder(140, 115, False))
        self.__ladders.append(Ladder(122, 84, False))

        #Mario
        self.__mario = Mario(MARIO_X,MARIO_Y)

        #Donkey Kong
        self.__donkeyKong = DonkeyKong(DK_X, DK_Y)

        #Pauline
        self.__pauline = Pauline(PAULINE_X, PAULINE_Y)

        #Run game
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        Function for calculations needed every frame
        Randomly creates barrels
        """
        if pyxel.btnp(pyxel.KEY_ESCAPE):                                        #Esc to quit game
            pyxel.quit()

        for pl in self.__platforms:
            self.mario_horizontal_movements(pl)
            self.mario_falls(pl)

        self.mario_vertical_movements()

        self.mario_jump()

        self.create_barrels()

        for bar in self.__barrels:
            self.barrel_movements(bar)
            self.barrel_ladder_falls(bar)

        self.delete_barrel()


    def draw(self):
        """
        Function for drawing things on the screen
        """
        pyxel.cls(0)                                                            #Background - black(0)

        #Draw platforms
        for platform in self.__platforms:
            platform.draw()

        #Draw ladders
        for ladder in self.__ladders:
            ladder.draw()

        #Draw barrel with fire
        pyxel.blt(7, 232, 0, 8, 2, 15, 13)
        pyxel.blt(8, 222, 0, 24, 4, 15, 10)

        #Draw Pauline
        self.__pauline.draw()

        #Draw static barrels at the top platform
        pyxel.blt(7, 73, 0, 12, 102, 10, 17)
        pyxel.blt(18, 73, 0, 12, 102, 10, 17)
        pyxel.blt(7, 57, 0, 12, 102, 10, 17)
        pyxel.blt(18, 57, 0, 12, 102, 10, 17)

        #Draw donkey king
        self.__donkeyKong.draw()

        #Draw bonus box
        pyxel.blt(150, 10, 0, 181, 99, 43, 20)
        #score = 0
        #pyxel.text(164, 20, str(score), 7)
        self.__mario.draw_score()
        
        #Draw lives
        #pyxel.blt(8, 10, 0, 131, 8, 7, 7)
        #pyxel.blt(17, 10, 0, 131, 8, 7, 7)
        #pyxel.blt(26, 10, 0, 131, 8, 7, 7)
        self.__mario.draw_lives()
        
        
        
        #Draw barrels
        for barrel in self.__barrels:
            barrel.draw()

        #Draw mario
        self.__mario.draw()


    def mario_horizontal_movements(self, platform):
        """
        Mario horizontal movements
        Right movement allowed only when Mario's x coordinate within borders
        and y coordinate appropriate for given platform
        Left movement allowed only when Mario's x coordinate within borders
        and y coordinate appropriate for given platform, on the first platform
        diferent border due to barrel with fire
        """
        if pyxel.btn(pyxel.KEY_RIGHT):
            if (self.__mario.x <= RIGHT_BORDER and                              #rigth border condition
            self.__mario.y == platform.y-MARIO_HEIGHT):                         #given plaform y coordinate condition
                self.__mario.move_right()
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.__mario.y == 230:                                           #if mario on the first platform
                if (self.__mario.x >= LEFT_BORDER+FIRE_WIDTH and                #left border with fire condition
                self.__mario.y == platform.y-MARIO_HEIGHT):                     #given plaform y coordinate condition
                    self.__mario.move_left()
            else:                                                               #other platforms
                if (self.__mario.x >= LEFT_BORDER and
                self.__mario.y == platform.y-MARIO_HEIGHT):
                    self.__mario.move_left()

    def mario_vertical_movements(self):
        """
        Mario vertical movements
        Up movement allowed only when Mario's x coordinate within range of
        one of the ladders width, y coordinate within range of one of the
        ladders height, ladder is not broken and mario is not jumping
        Down movement under the same conditions and up movement
        """
        for ld in self.__ladders:
            if pyxel.btn(pyxel.KEY_UP):
                if (self.__mario.x >= ld.x-7 and self.__mario.x <= ld.x+2 and   #ladder's width range conditions
                self.__mario.y <= ld.y-9 and self.__mario.y >= ld.y-39 and      #ladder's height range conditions
                ld.broken == False and not self.__mario.states["inJump"]):
                    self.__mario.move_up()
            elif pyxel.btn(pyxel.KEY_DOWN):
                if (self.__mario.x >= ld.x-7 and self.__mario.x <= ld.x+2 and
                self.__mario.y >= ld.y-40 and self.__mario.y <= ld.y-10 and
                ld.broken == False and not self.__mario.states["inJump"]):
                    self.__mario.move_down()

    def mario_falls(self, platform):
        """
        Mario falls
        Fall happen when Mario gets to the end of platform
        Fall movement lasts untill Mario's y coordinate value
        reaches platform below
        To prevent him from falling to low he can fall only when he is not
        in jump movement
        Right and left movements are allowed while in fall
        """
        if (self.__mario.x >= platform.endRight and not                         #end of platform on right condition
        self.__mario.states["inJump"] and self.__mario.y <= platform.y+15 and   #not in jump conditions and y coordinate conditions
        self.__mario.y >= platform.y-33):
            self.__mario.fall()
            if pyxel.btn(pyxel.KEY_RIGHT) and self.__mario.x <= RIGHT_BORDER:
                self.__mario.move_right()
            elif (pyxel.btn(pyxel.KEY_LEFT) and
            self.__mario.x >= platform.endRight+1):                             #left movement allowed only to endRight coordinate
                self.__mario.move_left()
        elif (self.__mario.x <= platform.endLeft-12 and not                     #end of platform on left condition
        self.__mario.states["inJump"] and self.__mario.y <= platform.y+15 and   #not in jump conditions and y coordinate conditions
        self.__mario.y >= platform.y-33):
            self.__mario.fall()
            if (pyxel.btn(pyxel.KEY_RIGHT) and
            self.__mario.x <= platform.endLeft-13):                             #right movement allowed only to endLeft coordinate
                self.__mario.move_right()
            elif pyxel.btn(pyxel.KEY_LEFT) and self.__mario.x >= LEFT_BORDER:
                self.__mario.move_left()

    def mario_jump(self):
        """
        Mario jump
        Jump movement when Space once pressed => inJump is set
        Right and left movements are allowed while in jump
        Jumps allowed only on platforms
        """
        if (pyxel.btn(pyxel.KEY_SPACE) and
        self.__mario.y in MARIO_PLATFORMS):                                     #jumps only on platforms condition
            self.__mario.states["inJump"] = True

        if (self.__mario.states["inJump"] == True and not
        self.__mario.states["isUp"]):                                           #ascend (jumpUp) until top (isUp)
            self.__mario.jumpUp()
            if pyxel.btn(pyxel.KEY_RIGHT) and self.__mario.x <= RIGHT_BORDER:   #left and right movements allowed while in jumpUp
                    self.__mario.move_right()
            elif pyxel.btn(pyxel.KEY_LEFT) and self.__mario.x >= LEFT_BORDER:
                    self.__mario.move_left()
        elif self.__mario.states["isUp"]:                                       #descend (jumpDown) until bottom (not isUp)
            self.__mario.jumpDown()
            if pyxel.btn(pyxel.KEY_LEFT) and self.__mario.x >= LEFT_BORDER:     #left and right movements allowed while in jumpDown
                self.__mario.move_left()
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.__mario.x <= RIGHT_BORDER:
                self.__mario.move_right()

    def create_barrels(self):
        """
        Create barrels
        Randomly create barrels, allow only 10 barrels at the same time
        Call grab method to animate Donkey Kong movemets
        Create and grab only allowed when Donkey Kong in normal state so the
        animation cannot be doubled
        """
        if (pyxel.frame_count % randint(60,100) == 0 and
        len(self.__barrels) < 10 and self.__donkeyKong.states["normal"]):
            self.__donkeyKong.states["inGrab"] = True                           #if conditions are met, start DonkeyKong's grabing animation

        if self.__donkeyKong.states["inGrab"]:
            self.__donkeyKong.grab()

            if self.__donkeyKong.movementTime == 5:                             #create barrel when near the end of grabbing animation
                self.__barrels.append(Barrel(BARREL_X, BARREL_Y))

    def barrel_movements(self, barrel):
        """
        Barrels movements
        Barrel can roll left or rigth only if on one of the platforms and
        between left and right edge of the platorm
        Barrel rotates right on platform shorter from right side and left
        on platforms shorter on left side
        """
        for pl in self.__platforms:
            if barrel.y in [203, 141, 79] and barrel.x <= pl.endRight:          #if barrel on platform shorter from right (6,4,2 counting from bottom to top)
                barrel.move_right()                                             #barrel moves right
            elif ((barrel.x >= pl.endRight or barrel.x <= pl.endLeft-12)        #if barrel at the right or left edge of the platform
            and barrel.y <= pl.y+19 and barrel.y >= pl.y-33):                   #y coordinate conditions for the barrel not to fall to low
                barrel.fall()
            elif barrel.y in [234, 172, 110] and barrel.x >= pl.endLeft:        #if barrel on platform shorter from left and bottom (5,3,1 counting from bottom to top)
                barrel.move_left()                                              #barrel moves left
        if pyxel.frame_count % 3 == 0:                                          #animation condition, every 3 frames we change the animation of barrel to make the rotate
            if barrel.states["toRight"]:                                        #if barrel moves right, make rotateRight animation
                barrel.rotateRight()
            elif barrel.states["toLeft"]:                                       #if barrel moves left, make rotateLeft animation
                barrel.rotateLeft()

    def barrel_ladder_falls(self, barrel):
        """
        Barrels ladder falls
        Each barrel has prob atribute which if the same as the ladder it passes
        allows it to fall that ladder
        Prob for barrel and ladder can be number from range 1-4 which gives
        barrel 25% chance for falling on the ladder
        """
        for lad in self.__ladders:
            if (barrel.x >= lad.x-7 and barrel.x <= lad.x+2 and                 #check if barrel is next to one of the ladders
             barrel.y >= lad.y-40 and barrel.y <= lad.y-6 and
             barrel.prob == lad.prob):                                          #if it is, check if has the same prob value as the ladder (1,2,3,4)
                    barrel.fall()                                               #if all conditions are met, fall of the ladder

    def delete_barrel(self):
        """
        Delete barrel
        When barrel reaches the end point next to barrel with fire it
        disappears and object its is deleted from the list
        Always the firt created barrel is the first deleted - FIFO
        """
        if (len(self.__barrels) > 0 and self.__barrels[0].y == 234 and          #object can be deleted only if the list is not empty
         self.__barrels[0].x <= 24):                                            #when barrel reaches the end point, disappears
            self.__barrels.pop(0)
