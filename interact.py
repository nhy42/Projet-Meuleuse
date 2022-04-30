import model


# import event


def spawnObject(objID, World=None, Spawnables=None):
    if Spawnables is None:
        Spawnables = model.giveSpawnables()
    if World is None:
        World = model.giveWorld()
    done = False
    i = len(Spawnables) - 1
    while i >= 0 and not done:
        if Spawnables[i]["id"] == objID:
            model.addObjectToWorld(Spawnables[i]["x"], Spawnables[i]["y"], Spawnables[i]["vx"], Spawnables[i]["vy"],
                                   Spawnables[i]["type"], Spawnables[i]["size"], Spawnables[i]["positionType"],
                                   Spawnables[i]["properties"], World)
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
            # le suivant est laissé car on ne peut pas changer la propriété avec spawn
            model.addObjectToWorld(e["x"], e["y"], e["vx"], e["vy"], e["type"], e["size"], e["positionType"],
                                   e["properties"] if "menu" in e["properties"] else (e["properties"] + ["menu"]),
                                   World)
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
