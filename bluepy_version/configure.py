import os


class Config:

    def __init__(self):

        self.settings = {}
        self.has_settings = False

        if "ss_settings.cfg" in os.listdir():
            self.load_cfg()
            self.has_settings = True

    def load_cfg(self):

        cfg = []

        with open("ss_settings.cfg", "r") as fp:
            cfg = [i.replace('\n', '') for i in fp.readlines()]


        for line in cfg:
            key, value = line.split("=")
            self.settings[key] = value

    def save_cfg(self):

        with open("ss_settings.cfg", "w") as fp:
            out = []
            for elem in self.settings.keys():
                fp.write(str(elem) + "=" + str(self.settings[elem]) + "\n")

    def __str__(self):
        return str(self.settings)


##############################################################################
# List of configuration settings:
#       - BLE scan time (in seconds)
#       - MQTT server TCP Address & port
#       - MQTT topic
#       - Name of connected device(s?) & Address
#       - UUID of desired characteristic
#
#############################################################################

if __name__ == "__main__":
    x = Config()
    print(x)
    x.settings["TEST1"] = "SOMEBODY"
    x.settings["TEST2"] = "ONCE"
    x.settings["TEST3"] = "TOLD"
    x.settings["TEST4"] = "ME"
    x.save_cfg()
