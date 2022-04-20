import pygame
import model
import sound
import level
import file
import event


DISPLAY = ""  # pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
CLOCK = pygame.time.Clock()
# VIEWWORLD = []
VIEWTYPES = file.readJSONFile("assets/viewTypes.json")
SPRITES = {}
MTOPIXEL = 1  # meters to pixel constant -> attention pour les collisions ?


def initView(size, Sprites=None):
    if Sprites is None:
        Sprites = SPRITES
    event.log("Initiating Pygame")
    # pygame.mixer.pre_init(44100, 16, 2, 4096)  # ???? le son je crois
    # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    pygame.init()
    event.log(f"Set screen size to {size[0]}x{size[1]}")
    global DISPLAY  # pas bien, je sais, mais là j'ai pas le choix
    DISPLAY = pygame.display.set_mode(size)
    pygame.display.init()
    for key in VIEWTYPES:
        Sprites[key] = pygame.image.load(VIEWTYPES[key]["spritePath"]).convert_alpha()


def quitGame():
    pygame.quit()


def getNextTick():
    return CLOCK.tick(60)  # todo : prendre des réglages


def getEvents():
    return pygame.event.get()


def loadBackgroundToSprites(bgPath):
    internalLoadBackgroundToSprites(SPRITES, bgPath)


def internalLoadBackgroundToSprites(Sprites, bgPath):
    Sprites["background"] = pygame.image.load(bgPath)


def getModelWorld():
    return model.giveWorldToView()


def internalRefreshView(Sprites, Viewtypes):
    # todo : amélioration du refresh, en updatant seulement les zones modifiées
    DISPLAY.blit(Sprites["background"], (0, 0))
    # objects
    modelWord = getModelWorld()  # ceci est une référence
    for obj in modelWord:
        objType = obj["type"]
        DISPLAY.blit(Sprites[objType], (obj["x"] - Viewtypes[objType]["sizeX"] / 2,
                                        obj["y"] - Viewtypes[objType]["sizeY"] / 2))
    pygame.display.flip()


def update():
    internalRefreshView(SPRITES, VIEWTYPES)
