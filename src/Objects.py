from random import randint
import pyxel

class Object:
    """
    Virtual class from which inherit all the other classes
    Each object in game needs its x and y coordinates as well as getters
    and setter for them
    """
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x
    @y.setter
    def y(self, y):
        self.__y = y


class Platform(Object):
    """
    Class for platforms
    Each platform has x and y coordinates, length needed to draw it and ends
    to determine edges
    """
    def __init__(self, x, y, length):
        super().__init__(x,y)
        self.__length = length
        self.__endLeft = x
        self.__endRight = x+7*length

    def draw(self):
        """
        Function draws full platform depending on platform's length
        """
        for i in range(self.__length):
            pyxel.blt(self.x+i*7, self.y, 0, 0, 8, 7, 7)

    @property
    def length(self):
        return self.__length

    @property
    def endLeft(self):
        return self.__endLeft

    @property
    def endRight(self):
        return self.__endRight


class Ladder(Object):
    """
    Class for ladders
    Each ladder has x and y coordinates as well as broken atribute to determine
    wheter it is full or broken and prob atribute holding value from range 1-4
    for the probability of barrel rolling over it
    """
    def __init__(self, x, y, broken):
        super().__init__(x,y)
        self.__broken = broken
        self.__prob = randint(1,4)

    def draw(self):
        """
        Function draws full or broken ladder depending on ladder's broken
        atribute
        """
        if self.__broken:
            pyxel.blt(self.x, self.y, 0, 0, 18, 8, 6, colkey=0)
            pyxel.blt(self.x, self.y-18, 0, 0, 18, 8, 6, colkey=0)
        else:
            for i in range(4):
                pyxel.blt(self.x, self.y-6*i, 0, 0, 18, 8, 6, colkey=0)

    @property
    def broken(self):
        return self.__broken
    @property
    def prob(self):
        return self.__prob


class DonkeyKong(Object):
    """
    Class for Donkey Kong
    For drawing reasons has the states atribute, depending on the state,
    appropriate animation is drawn
    """
    def __init__(self, x, y):
        super().__init__(x,y)
        self.__states = {"normal": True, "toRight": False, "toLeft": False, "withBarrel": False, "inGrab": False}
        self.__movementTime = 30

    def draw(self):
        """
        Function draws appropriate Donkey Kong sprite depending on the state
        """
        if self.__states["normal"]:
            pyxel.blt(self.x, self.y, 0, 5, 57, 40, 33)
        elif self.__states["toLeft"]:
            pyxel.blt(self.x, self.y, 0, 53, 58, 43, 32)
        elif self.__states["withBarrel"]:
            pyxel.blt(self.x, self.y, 0, 104, 58, 40, 32)
        elif self.__states["toRight"]:
            pyxel.blt(self.x, self.y, 0, 53, 58, -43, 32)

    def grab(self):
        """
        Function changes Donkey Kong state over time, using movementTime
        atribute to animate throwing the barrel
        """
        if self.__movementTime > 20:
            self.__states["normal"] = False
            self.__states["toLeft"] = True
            self.__movementTime -= 1
        elif self.__movementTime <= 20 and self.__movementTime > 10:
            self.__states["toLeft"] = False
            self.__states["withBarrel"] = True
            self.__movementTime -= 1
        elif self.__movementTime <= 10 and self.__movementTime > 0:
            self.__states["withBarrel"] = False
            self.__states["toRight"] = True
            self.__movementTime -= 1
        else:
            self.__states["toRight"] = False
            self.__states["normal"] = True
            self.__states["inGrab"] = False
            self.__movementTime = 30

    @property
    def states(self):
        return self.__states
    @property
    def movementTime(self):
        return self.__movementTime
    @states.setter
    def states(self, states):
        self.__states = states


class Pauline(Object):
    """
    Class for Pauline
    """
    def __init__(self, x, y):
        super().__init__(x,y)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 6, 179, 15, 22)


class Barrel(Object):
    """
    Class for barrels
    has the x, y attribute, which are the cooridinates of the barrel
    the state attribute defines the actions of the barrel, if she is suposed to move right, left, and whiych direction it supposed to
    rotate and if it is falling.
    the prob attribute is the random number from 1 to 4, it is compared with the prob number from the ladder object. If the number is
    the same the barrel is going to fell on the ladder. It has 25% chances to do that, this is a reason we the genereted number is 1-4
    """
    def __init__(self, x, y):
        super().__init__(x,y)
        self.__prob = randint(1,4)
        self.__states = {"upLeft": True, "upRight": False, "downRight": False, "downLeft": False, "toRight": True, "toLeft": False}

    def draw(self):
        """
        this method draws the barrel, accorting to the state it is currently in.
        """
        if self.__states["upLeft"]:
            pyxel.blt(self.x, self.y, 0, 35, 105, 12, 11, colkey=0)
        elif self.__states["upRight"]:
            pyxel.blt(self.x, self.y, 0, 59, 105, 12, 11, colkey=0)
        elif self.__states["downRight"]:
            pyxel.blt(self.x, self.y, 0, 83, 105, 12, 11, colkey=0)
        elif self.__states["downLeft"]:
            pyxel.blt(self.x, self.y, 0, 107, 105, 12, 11, colkey=0)

    def move_right(self):
        """
        Simulates barrel right movement and changes it state
        """
        self.x = self.x + 0.25
        self.__states["toRight"] = True
        self.__states["toLeft"] = False

    def move_left(self):
        """
        Simulates barrel left movement and changes it state
        """
        self.x = self.x - 0.25
        self.__states["toRight"] = False
        self.__states["toLeft"] = True

    def fall(self):
        """
        Simulates the fall of the barrel
        """
        self.y = self.y + 1

    def rotateRight(self):
        """
        Simulates the rotating of the barrel to the right
        """
        if self.__states["upLeft"] == True:
            self.__states["upRight"] = True
            self.__states["upLeft"] = False
        elif self.__states["upRight"] == True:
            self.__states["downRight"] = True
            self.__states["upRight"] = False
        elif self.__states["downRight"] == True:
            self.__states["downLeft"] = True
            self.__states["downRight"] = False
        elif self.__states["downLeft"] == True:
            self.__states["upLeft"] = True
            self.__states["downLeft"] = False

    def rotateLeft(self):
        """
        Simulates the rotating of the barrel to the left
        """
        if self.__states["upLeft"] == True:
            self.__states["upLeft"] = False
            self.__states["downLeft"] = True
        elif self.__states["downLeft"] == True:
            self.__states["downRight"] = True
            self.__states["downLeft"] = False
        elif self.__states["downRight"] == True:
            self.__states["upRight"] = True
            self.__states["downRight"] = False
        elif self.__states["upRight"] == True:
            self.__states["upLeft"] = True
            self.__states["upRight"] = False


    @property
    def prob(self):
        return self.__prob
    @property
    def states(self):
        return self.__states

class Mario(Object):
    """
    Class for Mario
    For drawing reasons has the states atribute, depending on the state,
    appropriate animation is drawn
    """
    def __init__(self, x, y):
        super().__init__(x,y)
        self.__states = {"toRight": True, "toLeft": False, "toBack": False, "isUp": False, "inJump": False}
        self.__jumpHeight = 12
        self.__score = 0
        self.__lives = 3

    def draw(self):
        """
        Function draws appropriate Mario sprite depending on the state
        """
        if self.__states["toLeft"] == True:
            pyxel.blt(self.x, self.y, 0, 6, 32, 12, 15, colkey=0)
        if self.__states["toRight"] == True:
            pyxel.blt(self.x, self.y, 0, 6, 32, -12, 15, colkey=0)
        if self.__states["toBack"]:
            pyxel.blt(self.x, self.y, 0, 148, 33, 16, 15, colkey=0)


    def draw_score(self):
        """
        Function that shows the actual score in the box
        """
        pyxel.text(164, 20, str(self.__score), 7)
    
    def draw_lives(self):
        """
        Function displays the current number of mario lives 
        """
        if self.__lives == 3:   
            pyxel.blt(8, 10, 0, 131, 8, 7, 7)
            pyxel.blt(17, 10, 0, 131, 8, 7, 7)
            pyxel.blt(26, 10, 0, 131, 8, 7, 7)
        elif self.__lives == 2:
            pyxel.blt(8, 10, 0, 131, 8, 7, 7)
            pyxel.blt(17, 10, 0, 131, 8, 7, 7)
        elif self.__lives == 1:
            pyxel.blt(8, 10, 0, 131, 8, 7, 7)
    
    
    
    
    
    def move_right(self):
        """
        Function simulates Mario's right movement
        Changes Mario's x position and state for drawing purposes
        """
        self.__states["toRight"] = True
        self.__states["toLeft"] = False
        self.__states["toBack"] = False
        self.x = self.x + 1

    def move_left(self):
        """
        Function simulates Mario's left movement
        Changes Mario's x position and state for drawing purposes
        """
        self.__states["toRight"] = False
        self.__states["toLeft"] = True
        self.__states["toBack"] = False
        self.x = self.x - 1

    def move_up(self):
        """
        Function simulates Mario's up movement
        Changes Mario's y position and state for drawing purposes
        """
        self.__states["toRight"] = False
        self.__states["toLeft"] = False
        self.__states["toBack"] = True
        self.y = self.y - 1

    def move_down(self):
        """
        Function simulates Mario's down movement
        Changes Mario's y position and state for drawing purposes
        """
        self.__states["toRight"] = False
        self.__states["toLeft"] = False
        self.__states["toBack"] = True
        self.y = self.y + 1

    def fall(self):
        """
        Function simulates Mario's fall movement
        Changes Mario's y position
        """
        self.y = self.y + 1

    def jumpUp(self):
        """
        Function simulates Mario's up movement while jumpung
        Movement length depends on the jumpHeight atribute
        """
        self.__jumpHeight -= 1
        if self.__jumpHeight > 3:
            self.y = self.y - 1.5

        if self.__jumpHeight <= 0:
            self.states["isUp"] = True

    def jumpDown(self):
        """
        Function simulates Mario's down movement while jumpung
        Movement length depends on the jumpHeight atribute
        """
        self.__jumpHeight += 1
        if self.__jumpHeight > 4:
            self.y = self.y + 1.5

        if self.__jumpHeight == 12:
            self.states["isUp"] = False
            self.states["inJump"] = False

    @property
    def states(self):
        return self.__states
    @property
    def jumpHeight(self):
        return self.__jumpHeight
    @states.setter
    def states(self, states):
        self.__states = states
