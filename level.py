import file
import event


def getLevel(lvlName):
    return file.readJSONFile("assets/lvl/" + lvlName + ".lvl")

