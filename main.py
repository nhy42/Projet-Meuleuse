# eval("\x69\x6d\x70\x6f\x72\x74\x20\x63\x6f\x6e\x74\x72\x6f\x6c\x6c\x65\x72\x0a\x63\x6f\x6e\x74\x72\x6f\x6c\x6c\x65\x72\x2e\x72\x75\x6e\x28\x29")
import controller
import event


if __name__ == "__main__":
    event.log("Starting game")
    controller.firstUse()
    controller.restoreSettings()
    controller.init()
    controller.run()
    event.log("Exiting game")
