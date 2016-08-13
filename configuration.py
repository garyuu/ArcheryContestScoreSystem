import configparser

CONFIG_FILENAME = "settings.cfg"
Config = configparser.ConfigParser()
Config.read(CONFIG_FILENAME)

def ConfigSectionMap(section):
    sectionMap = dict()
    options = Config.options(section)
    for option in options:
        try:
            sectionMap[option] = Config.get(section, option)
            if sectionMap[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            sectionMap[option] = None
    return sectionMap

def get(section, option):
    return Config.get(section, option)
