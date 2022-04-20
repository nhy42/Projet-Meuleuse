import file
import event


def getLevel(lvlName):
    return file.readJSONFile("assets/lvl/" + lvlName + ".lvl")


def getBackgroundPath(lvlName):
    level = getLevel(lvlName)
    return level["background"]
