import math

import physics
import level
import file
import event

MODELWORLD = []
WORLDCONFIG = {}
idCounter = 0
G = 6.6743e-11  # N*m^2*kg^-2
MODELTYPES = file.readJSONFile("assets/modelTypes.json")


def getNewID():
    global idCounter
    idCounter += 1
    return idCounter


def internalInitModel(World, WorldConfig, lvlName):
    # todo
    levelConfig = level.getLevel(lvlName)
    del World[:]
    setObjectInWorld(World, levelConfig["objects"])
    WorldConfig.clear()
    setWorldconfig(WorldConfig, levelConfig["rules"])


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
    WorldClone = World.copy()
    for i in range(len(World)):
        if World[i]["positionType"] != 0:  # check if movable
            # update position
            if World[i]["positionType"] == 1:
                World[i]["x"] = World[i]["x"] + World[i]["vx"] * ms / 1000
                World[i]["y"] = World[i]["y"] + World[i]["vy"] * ms / 1000
                # update velocity

                # acceleration = calcAccelerationOnObject(World[i], WorldClone)  # todo
            elif World[i]["positionType"] == 2:
                pass  # besoin d'un timer global (au moins du chargement du niveau)


def calcAccelerationOnObject(objectID, World):  # retourne l'acceleration dans un tableau
    # todo
    currentObject = {}
    for i in range(len(World)):
        if World[i]["id"] == objectID:
            currentObject["x"] = World[i]["x"]
            currentObject["y"] = World[i]["y"]
            currentObject["mass"] = MODELTYPES[World[i]["type"]]["mass"]
            currentObject["type"] = World[i]["type"]
            # if pour les non-spheriques ^ todo
    for i in range(len(World)):
        # NE PAS OUBLIER DE FAIRE X2 SI L'OBJET EST IMMOBILE => en fait non
        # math.sqrt((currentObject["x"] - [World[i]["x"]])**2+(currentObject["y"] - World[i]["y"])**2)
        # todo
        pass


def giveWorldToView():
    return internGiveWorldToView(MODELWORLD)


def internGiveWorldToView(World):
    return World
