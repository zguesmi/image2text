import argparse, os, sys, subprocess, imghdr
from subprocess import call

import exceptions as exc
from consensus import Consensus
from ocr import OCR



class App:

    DATADIR = '/iexec/'
    CONFIG_FILE = DATADIR + 'config.txt'
    IN = DATADIR + 'in/'
    OUT = DATADIR + 'out/'
    EXT = '.txt'
    SUPPORTED_IMAGES = ['pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png']


    def fullPath(self, filename):
        return '{}{}'.format(self.DATADIR, filename)


    def inFullPath(self, filename):
        return '{}{}'.format(self.IN, filename)


    def outFullPath(self, filename):
        return '{}{}'.format(self.OUT, filename)


    def txtFullPath(self, filename):
        return '{}{}{}'.format(self.OUT, filename, self.EXT)


    def isNotConfigFile(self, f):
        return self.fullPath(f) != self.CONFIG_FILE


    def isSupportedImage(self, f):
        return ( os.path.isfile(self.fullPath(f))
            and self.isNotConfigFile(f)
            and imghdr.what(self.fullPath(f)) in self.SUPPORTED_IMAGES )


    def parseConfigFile(self):

        if not os.path.isfile(self.CONFIG_FILE):
            raise exc.NoConfigFileError

        f = open(self.CONFIG_FILE)
        for line in f:
            try:
                conf = list(map(str.strip, line.split(':')))
            except Exception:
                raise exc.UnrespectedConfigFormatError
            if(len(conf) != 2):
                raise exc.UnrespectedConfigFormatError

            self.config.append(conf)


    def prepareDatadir(self):
    
        try:
            os.mkdir(self.IN)

            for f in [ f for f in os.listdir(self.DATADIR) if self.isSupportedImage(f) ]:
                call([ 'mv', self.fullPath(f), self.IN ])

            os.mkdir(self.OUT)

        except Exception:
            raise exc.FatalError
            

    def __init__(self):

        self.config = []
        self.parseConfigFile()
        self.prepareDatadir()


    def save(self, filename, text):

        try:
            file = open(self.txtFullPath(filename), 'wb')
            file.write(text)
        except Exception:
            raise exc.CanNotSaveTextError()
        finally:
            file.close()


    def main(self):

        for config in self.config:
            try:

                if not os.path.isfile('{}{}'.format(self.IN, config[0])):
                    raise exc.FileNotFoundError(config[0])

                text = OCR().imageToString(path=self.inFullPath(config[0]), lang=config[1])
                self.save(filename=config[0], text=text)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    App().main()
    Consensus().create()