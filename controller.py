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
        update()
    event.log("End of main loop")
    view.quitGame()


def update():
    # NE PAS OUBLIER DE FAIRE SAUTER LA PREMIERE ITERATION (ou pas osef en fait)
    ms = view.getNextTick()
    model.updateModel(ms)
    # update the model
    # render
    view.initLevel()


def firstUse():
    event.warn("TODO: First Use")
    if not firstUse:
        event.log("First use")
        pass
        # ask for settings (taille de l'ecran, etc)
    else:
        event.log("Not first use")


def init():
    # restore les paramètres
    view.initView((1280, 720))
    model.initModel("splashScreen")


def restoreSettings():
    return internalRestoreSettings(SETTINGS)


def internalRestoreSettings(Settings):
    Settings = file.readJSONFile("userdata/settings.json")
    return 0


# def saveSettings(settings):  # ?
#     pass
