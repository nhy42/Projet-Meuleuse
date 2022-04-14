import controller
import event


if __name__ == "__main__":
    event.log("Starting game")
    controller.firstUse()
    controller.restoreSettings()
    controller.init()
    controller.run()
    event.log("Exiting game")
