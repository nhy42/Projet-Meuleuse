import pygame
import model
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
        if "invisible" not in VIEWTYPES[key]:
            Sprites[key] = pygame.image.load(VIEWTYPES[key]["spritePath"]).convert_alpha()


def quitGame():
    pygame.quit()


def getNextTick():
    return CLOCK.tick(60)  # todo : prendre des réglages


def getEvents():
    return pygame.event.get()


def getEventsParsed():
    events = getEvents()
    if len(events) != 0:  # opti, souvent pas d'interraction => physique allumée
        parsedEvents = []
        for e in events:
            daEvent = []
            if e.type == pygame.MOUSEBUTTONDOWN:
                daEvent.append("MOUSEBUTTONDOWN")
            elif e.type == pygame.MOUSEBUTTONUP:
                daEvent.append("MOUSEBUTTONUP")
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    daEvent.append("KEYDOWN")
                    daEvent.append("BACKSPACE")
                elif e.key == pygame.K_ESCAPE:
                    daEvent.append("KEYDOWN")
                    daEvent.append("ESCAPE")
                elif e.key == pygame.K_SPACE:
                    daEvent.append("KEYDOWN")
                    daEvent.append("SPACE")
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_BACKSPACE:
                    daEvent.append("KEYUP")
                    daEvent.append("BACKSPACE")
                elif e.key == pygame.K_ESCAPE:
                    daEvent.append("KEYUP")
                    daEvent.append("ESCAPE")
                elif e.key == pygame.K_SPACE:
                    daEvent.append("KEYUP")
                    daEvent.append("SPACE")
            if len(daEvent) > 0:
                parsedEvents.append(daEvent)
        return parsedEvents
    else:
        return []


def getMousePos():
    return pygame.mouse.get_pos()


def loadBackgroundToSprites(bgPath):
    internalLoadBackgroundToSprites(SPRITES, bgPath)


def internalLoadBackgroundToSprites(Sprites, bgPath):
    Sprites["background"] = pygame.image.load(bgPath)


def getModelWorld():
    return model.giveWorld()


def internalRefreshView(Sprites, Viewtypes):
    # todo : amélioration du refresh, en updatant seulement les zones modifiées
    DISPLAY.blit(Sprites["background"], (0, 0))
    # objects
    modelWord = getModelWorld()  # ceci est une référence
    for obj in modelWord:
        objType = obj["type"]
        if "invisible" not in VIEWTYPES[objType]:
            DISPLAY.blit(Sprites[objType], (obj["x"] - Viewtypes[objType]["sizeX"] / 2,
                                            obj["y"] - Viewtypes[objType]["sizeY"] / 2))
    pygame.display.flip()


def update():
    internalRefreshView(SPRITES, VIEWTYPES)
