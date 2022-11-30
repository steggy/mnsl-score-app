from configparser import ConfigParser

class Config():
    def __init__(self,cfile):
        self.cfile = cfile

    def Fetch(self,sect):
        config = ConfigParser()
        config.read(self.cfile)
        #out = [tup[1] for tup in list(config.items(sect))]
        #return out
        return list(config.items(sect))


    def Update(self,sect,keyvaluedict):
        config = ConfigParser()
        config.read(self.cfile)
        for x, y in keyvaluedict.items():
            config.set(sect,x,y)
        with open(self.cfile,'w') as configfile:
            config.write(configfile)

