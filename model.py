import view
import physics
import level
import file
import event


MODELWORLD = []
WORLDCONFIG = {}
idCounter = 0  # donc le compteur commence à 1
MODELTYPES = file.readJSONFile("assets/modelTypes.json")


def getNewID():
    global idCounter
    idCounter += 1
    return idCounter


def internalInitModel(World, WorldConfig, lvlName):
    levelConfig = level.getLevel(lvlName)
    del World[:]
    setObjectInWorld(World, levelConfig["objects"])
    WorldConfig.clear()
    setWorldconfig(WorldConfig, levelConfig["rules"])  # todo
    view.loadBackgroundToSprites(levelConfig["background"])


def setObjectInWorld(World, objects):
    for obj in objects:
        World.append({"id": getNewID(),
                      "x": obj["x"],
                      "y": obj["y"],
                      "vx": obj["vx"],
                      "vy": obj["vy"],
                      "type": obj["type"],
                      "size": obj["size"],
                      "positionType": obj["positionType"]
                      })


def setWorldconfig(WorldConfig, configToImport):
    for rule in configToImport:
        # WorldConfig[]  # todo here
        pass


def initModel(lvlName):
    event.log(f"Loading level {lvlName}")
    return internalInitModel(MODELWORLD, WORLDCONFIG, lvlName)


def updateModel(ms):
    return internalUpdateModel(MODELWORLD, WORLDCONFIG, ms)


def internalUpdateModel(World, WorldConfig, ms):
    # do other updates and checks
    # get events
    if "noPhysics" not in WorldConfig:
        updatePositions(World, ms)


def updatePositions(World, ms):
    for i in range(len(World)):
        if World[i]["positionType"] != 0:  # check if movable  todo : opti
            # update position
            if World[i]["positionType"] == 1:

                tempX = World[i]["x"] + World[i]["vx"] * ms / 1000
                tempY = World[i]["y"] + World[i]["vy"] * ms / 1000

                # todo : collision
                collided = physics.isColliding(World, tempX, tempY, MODELTYPES[World[i]["type"]]["r"])
                if len(collided) != 0:
                    # event.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH")
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


def giveWorldToView():
    return internGiveWorldToView(MODELWORLD)


def internGiveWorldToView(World):
    return World
