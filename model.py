import view
import physics
import interact
import level
import file
import event

MODELWORLD = []
SPAWNABLES = []
WORLDCONFIG = {}
idCounter = 0  # donc le compteur commence à 1
MODELTYPES = file.readJSONFile("assets/modelTypes.json")


def getNewID():
    global idCounter
    idCounter += 1
    return idCounter


def internalInitModel(World, WorldConfig, Spawnables, lvlName):
    levelConfig = level.getLevel(lvlName)
    # World
    del World[:]
    setObjectsInWorld(World, levelConfig["objects"])
    # Spawnables
    del Spawnables[:]
    for e in levelConfig["spawnables"]:
        Spawnables.append(e)
    # WorldConfig
    WorldConfig.clear()
    setWorldconfig(WorldConfig, levelConfig["rules"], lvlName)
    view.loadBackgroundToSprites(levelConfig["background"])


def setObjectsInWorld(World, objects):
    for obj in objects:
        addObjectToWorld(obj, World)


def addObjectToWorld(obj, World=None):
    if World is None:
        World = giveReference(MODELWORLD)
    objCopy = obj.copy()
    objCopy["id"] = getNewID()
    World.append(objCopy)


def setWorldconfig(WorldConfig, configToImport, lvlName):
    WorldConfig["lvlName"] = lvlName
    for rule in configToImport:
        WorldConfig[rule] = ""


def initModel(lvlName):
    event.log(f"Loading level {lvlName}")
    return internalInitModel(MODELWORLD, WORLDCONFIG, SPAWNABLES, lvlName)


def updateModel(ms):
    return False if internalUpdateModel(MODELWORLD, WORLDCONFIG, SPAWNABLES, ms) == -1 else True


def internalUpdateModel(World, WorldConfig, Spawnables, ms):
    # get events
    events = view.getEventsParsed()
    mouseX, mouseY = view.getMousePos()

    # event processing
    leavingThisUpdate = processUserEvents(World, WorldConfig, Spawnables, events, mouseX, mouseY)
    if leavingThisUpdate:
        return 1
    for e in events:
        if e[0] == "LEAVE":
            return -1

    for i in range(len(World)):
        if "dragged" in World[i]["properties"] and \
                (("displayingMenu" in WorldConfig) == ("menu" in World[i]["properties"])):
            World[i]["x"] = mouseX
            World[i]["y"] = mouseY

    if "noPhysics" not in WorldConfig:
        updatePositions(World, WorldConfig, ms)


def processUserEvents(World, WorldConfig, Spawnables, events, mx, my):
    for e in events:
        if e[0] == "MOUSEBUTTONDOWN":
            i = len(World) - 1
            while i >= 0:
                if "onClick" in World[i]:
                    if physics.isInside(World[i], mx, my):
                        leaveThisUpdate = interact.processEventsToDo(World[i]["onClick"], World[i]["id"],
                                                                     World, WorldConfig, Spawnables)
                        if leaveThisUpdate:
                            return True
                i -= 1
        elif e[0] == "MOUSEBUTTONUP":
            interact.undragObject(World, WorldConfig)
        elif e[0] == "KEYDOWN":
            if e[1] == "BACKSPACE":
                if "allowReloadKey" in WorldConfig:
                    interact.reloadLevel(WorldConfig)
            elif e[1] == "SPACE":
                if "allowPauseKey" in WorldConfig:
                    interact.switchPause(World, WorldConfig, Spawnables)
            elif e[1] == "ESCAPE":
                if "allowMenuKey" in WorldConfig:
                    interact.switchMenu(World, WorldConfig, Spawnables)
        elif e[0] == "KEYUP":
            pass  # pour future utilisation (ou pas ?)


# def processCollisionEvent(Object):
#     pass
#     # je sais pas ce que tu es mais en tout cas j'ai perdu l'idée, ca c'est sur


def updatePositions(World, WorldConfig, ms):
    for i in range(len(World)):
        if World[i]["positionType"] != 0 and \
                (("displayingMenu" in WorldConfig) == ("menu" in World[i]["properties"]) == ("paused" in WorldConfig)) \
                and "dragged" not in World[i]["properties"]:
            # update position
            if World[i]["positionType"] == 1:

                tempX = World[i]["x"] + World[i]["vx"] * ms / 1000
                tempY = World[i]["y"] + World[i]["vy"] * ms / 1000

                collided = physics.isCollidingSomething(World, tempX, tempY, MODELTYPES[World[i]["type"]]["r"], World[i]["type"], World[i]["id"])

                if len(collided) == 3:
                    collisionResult = physics.calcCollision(World[i]["x"], World[i]["y"],
                                                            MODELTYPES[World[i]["type"]]["r"],
                                                            World[i]["vx"], World[i]["vy"],
                                                            collided[0], collided[1], collided[2],
                                                            MODELTYPES[World[i]["type"]]["friction"], ms)
                    # ^ retourne [newX, newY, newVX, newVY]
                    World[i]["x"], World[i]["y"] = collisionResult[0], collisionResult[1]
                    World[i]["vx"], World[i]["vy"] = collisionResult[2], collisionResult[3]
                elif len(collided) == 1:  # si des events collision ont été cassant
                    return 0
                else:
                    World[i]["x"] = tempX
                    World[i]["y"] = tempY

                # update velocity
                ax, ay = physics.calcAccelerationOnObject(World[i]["id"], World, WorldConfig)
                World[i]["vx"] = World[i]["vx"] + ax * ms / 1000
                World[i]["vy"] = World[i]["vy"] + ay * ms / 1000


def giveWorld():
    return giveReference(MODELWORLD)


def giveWorldConfig():
    return giveReference(WORLDCONFIG)


def giveSpawnables():
    return giveReference(SPAWNABLES)


def giveReference(obj):
    return obj
