import argparse, os, sys, subprocess, imghdr, yaml
from subprocess import call

import exceptions as exc
from consensus import Consensus
from ocr import OCR



class App:

    APP_CONFIG = '../app-config.yml'
    _SUPPORTED_IMAGES = ['pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png']


    def __init__(self):

        yml = yaml.load(open(self.APP_CONFIG))

        self._datadir = '{}/'.format( yml['datadir'] )
        self._inputConfigFile = '{}/{}'.format( yml['datadir'], yml['input-config'] )
        self._in = '{}/{}/'.format( yml['datadir'], yml['input-dir'] )
        self._out = '{}/{}/'.format( yml['datadir'], yml['output-dir'] )
        self._outputFileExtension = yml['output-files-extension']
        self._inputConfig = []

        self.parseConfigFile()
        self.prepareDatadir()


    def fullPath(self, filename):
        return '{}{}'.format(self._datadir, filename)


    def isNotConfigFile(self, filename):
        return self.fullPath(filename) != self._inputConfigFile


    def isSupportedImage(self, filename):
        return ( os.path.isfile(self.fullPath(filename))
            and self.isNotConfigFile(filename)
            and imghdr.what( self.fullPath(filename) ) in self._SUPPORTED_IMAGES )


    def parseConfigFile(self):

        if not os.path.isfile(self._inputConfigFile):
            raise exc.NoConfigFileError

        f = open(self._inputConfigFile)
        for line in f:
            try:
                conf = list(map(str.strip, line.split(':')))
            except Exception:
                raise exc.UnrespectedConfigFormatError
            if(len(conf) != 2):
                raise exc.UnrespectedConfigFormatError

            self._inputConfig.append(conf)


    def prepareDatadir(self):
    
        try:
            os.mkdir(self._in)

            for f in [ f for f in os.listdir(self._datadir) if self.isSupportedImage(f) ]:
                call([ 'mv', self.fullPath(f), self._in ])

            os.mkdir(self._out)

        except Exception:
            raise exc.FatalError


    def save(self, filename, text):

        try:
            path = '{}{}.{}'.format( self._out, filename, self._outputFileExtension )
            fp = open(path, 'wb')
            fp.write(text)
        except Exception:
            raise exc.CanNotSaveTextError()
        finally:
            fp.close()


    def main(self):

        for conf in self._inputConfig:
            try:

                if not os.path.isfile('{}{}'.format(self._in, conf[0])):
                    raise exc.FileNotFoundError(conf[0])

                path = '{}{}'.format(self._in, conf[0])
                text = OCR().imageToString(path=path, lang=conf[1])
                self.save(filename=conf[0], text=text)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = App()
    app.main()
    Consensus(app.APP_CONFIG).create()