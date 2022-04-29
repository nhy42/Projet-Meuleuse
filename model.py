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
        spawnObjet(obj["x"], obj["y"], obj["vx"], obj["vy"], obj["type"], obj["size"], obj["positionType"],
                   obj["properties"] if "properties" in obj else [], World)


def spawnObjet(x, y, vx, vy, objectType, size, positionType, properties, World=None):
    if World is None:
        World = giveReference(MODELWORLD)
    World.append({"id": getNewID(),
                  "x": x,
                  "y": y,
                  "vx": vx,
                  "vy": vy,
                  "type": objectType,
                  "size": size,
                  "positionType": positionType,
                  "properties": properties})


def setWorldconfig(WorldConfig, configToImport, lvlName):
    WorldConfig["lvlName"] = lvlName
    for rule in configToImport:
        WorldConfig[rule] = ""


def initModel(lvlName):
    event.log(f"Loading level {lvlName}")
    return internalInitModel(MODELWORLD, WORLDCONFIG, SPAWNABLES, lvlName)


def updateModel(ms):
    return internalUpdateModel(MODELWORLD, WORLDCONFIG, SPAWNABLES, ms)


def internalUpdateModel(World, WorldConfig, Spawnables,  ms):
    # get events
    events = view.getEventsParsed()
    mouseX, mouseY = view.getMousePos()

    # event processing
    processUserEvents(World, WorldConfig, events, mouseX, mouseY)

    if "noPhysics" not in WorldConfig:
        updatePositions(World, ms)


def processUserEvents(World, WorldConfig, events, mx, my):
    for e in events:
        if e[0] == "MOUSEBUTTONDOWN" or e[0] == "MOUSEBUTTONUP":
            pass
        elif e[0] == "KEYDOWN":
            if e[1] == "BACKSPACE":
                pass
            elif e[1] == "SPACE":
                pass
            elif e[1] == "ESCAPE":
                pass
        elif e[0] == "KEYUP":
            pass  # pour future utilisation (ou pas ?)


def processCollisionEvent(Object):
    pass


def updatePositions(World, ms):
    for i in range(len(World)):
        if World[i]["positionType"] != 0:
            # check if movable  todo : opti
            # update position
            if World[i]["positionType"] == 1:

                tempX = World[i]["x"] + World[i]["vx"] * ms / 1000
                tempY = World[i]["y"] + World[i]["vy"] * ms / 1000

                collided = physics.isCollidingSomething(World, tempX, tempY, MODELTYPES[World[i]["type"]]["r"])
                if len(collided) != 0:
                    collisionResult = physics.calcCollision(World[i]["x"], World[i]["y"],
                                                            MODELTYPES[World[i]["type"]]["r"],
                                                            World[i]["vx"], World[i]["vy"],
                                                            collided[0], collided[1], collided[2],
                                                            MODELTYPES[World[i]["type"]]["friction"], ms)
                    # ^ retourne [newX, newY, newVX, newVY]
                    World[i]["x"], World[i]["y"] = collisionResult[0], collisionResult[1]
                    World[i]["vx"], World[i]["vy"] = collisionResult[2], collisionResult[3]
                else:
                    World[i]["x"] = tempX
                    World[i]["y"] = tempY

                # update velocity
                ax, ay = physics.calcAccelerationOnObject(World[i]["id"], World)
                World[i]["vx"] = World[i]["vx"] + ax * ms / 1000
                World[i]["vy"] = World[i]["vy"] + ay * ms / 1000


def giveWorld():
    return giveReference(MODELWORLD)


def giveWorldConfig():
    return giveReference(WORLDCONFIG)


def giveReference(obj):
    return obj
