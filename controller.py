import view
import model
import file
import event

SETTINGS = {}


def run():
    event.log("Begin running")
    # main game loop
    keepRunning = True
    event.log("Main loop starting")
    while keepRunning:
        keepRunning = update()
    event.log("End of main loop")
    view.quitGame()


def update():
    # NE PAS OUBLIER DE FAIRE SAUTER LA PREMIERE ITERATION (ou pas osef en fait)
    ms = view.getNextTick()
    # print(ms)
    # update the model
    keep = model.updateModel(ms)
    # render
    view.update()
    return keep


def firstUse():
    # todo : first use
    if not firstUse:
        event.log("First use")
        pass
        # ask for settings (taille de l'ecran, etc)
    else:
        event.log("Not first use")


def init():
    # restore les paramètres
    view.initView((1920, 1080))
    model.initModel("lvlmenu")
    view.update()


def restoreSettings():
    return internalRestoreSettings(SETTINGS)


def internalRestoreSettings(Settings):
    Settings = file.readJSONFile("userdata/settings.json")
    return 0

# def saveSettings(settings):  # ?
#     pass
