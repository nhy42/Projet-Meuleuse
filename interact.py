import model
import file
import physics
# import event

MODELTYPES = file.readJSONFile("assets/modelTypes.json")
SECURITYRADIUSCONST = 55  # rayon de la balle + boh jsais pas 5
# ^ pour l'instant, dans le futur faire r de la plus grosse balle + 5~10


def spawnObject(objID, World=None, Spawnables=None):
    if Spawnables is None:
        Spawnables = model.giveSpawnables()
    if World is None:
        World = model.giveWorld()
    done = False
    i = len(Spawnables) - 1
    while i >= 0 and not done:
        if Spawnables[i]["id"] == objID:
            model.addObjectToWorld(Spawnables[i], World)
            done = True
        i -= 1


def deleteObjectByTag(tag, World=None):
    if World is None:
        World = model.giveWorld()
    i = len(World) - 1
    while i >= 0:  # end -> beginning
        if tag in World[i]["properties"]:
            del World[i]
        i -= 1


def reloadLevel(WorldConfig):
    model.initModel(WorldConfig["lvlName"])


def switchMenu(World, WorldConfig, Spawnables):
    if "displayingMenu" in WorldConfig:
        hideMenu(World, WorldConfig)
    else:
        popMenu(World, WorldConfig, Spawnables)


def popMenu(World, WorldConfig, Spawnables):
    # event.log("Menu popped")
    pauseGame(World, WorldConfig, Spawnables)
    for e in Spawnables:
        if 100 <= e["id"] < 200:
            model.addObjectToWorld(e, World)
    WorldConfig["displayingMenu"] = ""


def hideMenu(World, WorldConfig):
    # event.log("Menu hidden")
    deleteObjectByTag("menu", World)
    WorldConfig.pop("displayingMenu", None)
    # ^ si la propriété n'est pas présente (ne doit pas arriver), retourne None


def switchPause(World, WorldConfig, Spawnables):
    if "paused" in WorldConfig:
        unpauseGame(World, WorldConfig, Spawnables)
    else:
        pauseGame(World, WorldConfig, Spawnables)


def pauseGame(World, WorldConfig, Spawnables):
    if "paused" not in WorldConfig:
        WorldConfig["paused"] = ""
        if "dontShowPauseSign" not in WorldConfig:
            deleteObjectByTag("pauseSign", World)
            spawnObject(200, World, Spawnables)


def unpauseGame(World, WorldConfig, Spawnables):
    if "displayingMenu" not in WorldConfig:
        WorldConfig.pop("paused", None)
        if "dontShowPauseSign" not in WorldConfig:
            deleteObjectByTag("pauseSign", World)
            spawnObject(201, World, Spawnables)


def dragObject(objID, World, WorldConfig):
    for i in range(len(World)):
        if objID == World[i]["id"] and "dragged" not in World[i]["properties"] and "dragging" not in WorldConfig:
            World[i]["properties"].append("dragged")
            WorldConfig["dragging"] = ""


def undragObject(World, WorldConfig):
    # verif les distances et tt, si oui faire, sinon rien
    if "dragging" in WorldConfig:
        for i in range(len(World)):
            if "dragged" in World[i]["properties"]:
                canDo = True
                for obj in World:  # enlever l'objet courant
                    if MODELTYPES[obj["type"]]["type"] == 1 and obj["id"] != World[i]["id"]:
                        d = physics.mesureDistance(World[i]["x"], World[i]["y"], obj["x"], obj["y"]) \
                            - (MODELTYPES[World[i]["type"]]["r"] + MODELTYPES[obj["type"]]["r"])
                        if d < SECURITYRADIUSCONST:
                            canDo = False
                if canDo:
                    World[i]["properties"].remove("dragged")
                    WorldConfig.pop("dragging", None)


def addRule(WorldConfig, rule):
    if rule not in WorldConfig:
        WorldConfig[rule] = ""


def delRule(WorldConfig, rule):
    if rule in WorldConfig:
        del WorldConfig[rule]


def processEventsToDo(eventsString, objID, World=None, WorldConfig=None, Spawnables=None):
    if World is None:
        World = model.giveWorld()
    if WorldConfig is None:
        WorldConfig = model.giveWorldConfig()
    if Spawnables is None:
        Spawnables = model.giveSpawnables()
    for e in eventsString.split(" "):
        splited = e.split("_")
        if e == "drag":
            dragObject(objID, World, WorldConfig)
        elif splited[0] == "loadLevel":
            model.initModel(splited[1])
            return True
            # on arrete l'iteration pour ne pas boucler sur des éléments du nouveau niveau
        elif splited[0] == "spawnObject":
            for oID in splited[1:]:
                spawnObject(oID, World, Spawnables)
        elif splited[0] == "delObject":
            for tag in splited[1:]:
                deleteObjectByTag(tag, World)
        elif splited[0] == "addRules":
            for rule in splited[1:]:
                addRule(WorldConfig, rule)
        elif splited[0] == "delRules":
            for rule in splited[1:]:
                delRule(WorldConfig, rule)
