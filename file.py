import json


def readJSONFile(path):
    with open(path, "r") as f:
        jsonObject = json.load(f)
    return jsonObject


def saveIntoJSON(path, dictionary):
    dataToWrite = json.dumps(dictionary)
    with open(path, "w") as f:
        f.write(dataToWrite)
    return 0


