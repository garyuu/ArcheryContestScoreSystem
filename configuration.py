'''
Author: Garyuu
Date:   2016/8/13
Name:   configuration
Descr.: Config will load whole config file.
        SectionConfig can be used to load only one section.
'''
import configparser

class Config(configparser.ConfigParser):
    filename = ''
    
    def __init__(self, filename):
        configparser.ConfigParser.__init__(self)
        self.filename = filename
        self.read(filename + '.cfg')

class SectionConfig(Config):
    section = ''
    sectionMap = dict()

    def __init__(self, filename, section):
        Config.__init__(self, filename)
        self.section = section
        self.buildSectionMap()

    def buildSectionMap(self):
        options = self.options(self.section)
        for option in options:
            try:
                self.sectionMap[option] = self.get(self.section, option)
                if self.sectionMap[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                self.sectionMap[option] = None

    def __getitem__(self, index):
        return self.sectionMap[index]
