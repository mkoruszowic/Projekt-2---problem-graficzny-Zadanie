from os import path

# ustawienia gry
TITLE = "GEO DASH"
WIDTH = 800
HEIGHT = 500
FPS = 60
SPRITESHEET = "spritesheet.png"
FONT_NAME = "arial"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# właściwości gracza
PLAYER_GRAV = 1.5
PLAYER_SPEED = 8
PLAYER_JUMP = 23

# tworzenie poziomu
PLATFORM_LIST = list()
SPIKE_LIST = list()
ORB_LIST = list()
BOOST_LIST = list()

poziom1 = 1
game_file = path.dirname(__file__)
s = open(path.join(game_file, "LEVEL" + str(poziom1) + ".txt"), "r")
read = s.read()
G_LENGTH = read.count("p") +  read.count("P")

class Level:
    def __init__(self):
        self.G_LENGTH = 0

    def create(self, poziom):
        self.poziom = poziom
        level_file = open(path.join(game_file, "LEVEL" + str(self.poziom) + ".txt"), "r")
        k = 0
        l = 0

        for line in level_file:
            for character in line:
                if character == "p":
                    PLATFORM_LIST.append((k * 50, HEIGHT - 50 - (l * 50), 50, 50, 0))
                elif character == "P":
                    PLATFORM_LIST.append((k * 50, HEIGHT - 50 - (l * 50), 50, 25, 1))
                elif character == "s":
                    SPIKE_LIST.append((k * 50, HEIGHT - 25 - (l * 50), 50, 50))
                elif character == "o":
                    ORB_LIST.append((k * 50, HEIGHT - 50 - (l * 50), 60, 60))
                elif character == "b":
                    BOOST_LIST.append((k * 50, HEIGHT - 50 - (l * 50), 50, 50))
                l += 1
            k += 1
            l = 0

lvl = Level()
lvl.create(poziom1)
