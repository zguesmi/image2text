import os, sys, subprocess, imghdr, yaml

import exceptions as exc
from consensus import Consensus
from ocr import OCR



class App:

    APP_CONFIG = '../app-config.yml'
    _SUPPORTED_IMAGES = ['pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png']


    def __init__(self):

        yml = yaml.load(open(self.APP_CONFIG))

        self._datadir = yml['datadir']
        self._inputConfigFile = yml['input-config']
        self._inputConfigFilePath = '{}/{}'.format( yml['datadir'], yml['input-config'] )
        self._in = '{}/{}'.format( yml['datadir'], yml['input-dir'] )
        self._out = '{}/{}'.format( yml['datadir'], yml['output-dir'] )
        self._outputFileExtension = yml['output-files-extension']
        self._inputConfig = self.parseConfigFile()

        # print(self._inputConfig)
        # sys.exit('you told me that')

        self.prepareDatadir()


    def fullPath(self, filename):
        return '{}/{}'.format( self._datadir, filename )


    def inFullPath(self, filename):
        return '{}/{}'.format( self._in, filename )


    def outFullPath(self, filename):
        return '{}/{}.{}'.format( self._out, filename, self._outputFileExtension )


    def isNotConfigFile(self, filename):
        return self.fullPath(filename) != self._inputConfigFilePath


    def isSupportedImage(self, filename):
        return ( os.path.isfile(self.fullPath(filename))
            and imghdr.what( self.fullPath(filename) ) in self._SUPPORTED_IMAGES
            and self.isNotConfigFile(filename) )


    def parseConfigFile(self):

        if not os.path.isfile(self._inputConfigFilePath):
            raise exc.ConfigFileNotFoundError(self._inputConfigFile)

        try:
            return yaml.load(open(self._inputConfigFilePath))
        except Exception as e:
            raise exc.UnrespectedConfigFormatError(e)


    def prepareDatadir(self):
    
        try:
            os.mkdir(self._in)

            for f in [ f for f in os.listdir(self._datadir) if self.isSupportedImage(f) ]:
                call([ 'mv', self.fullPath(f), self._in ])

            os.mkdir(self._out)

        except Exception as e:
            raise exc.FatalError(e)


    def save(self, filename, text):

        try:
            path = self.outFullPath(filename)
            fp = open(path, 'wb')
            fp.write(text)
        except Exception as e:
            raise exc.CanNotSaveTextError(e, path)
        finally:
            fp.close()


    def main(self):

        for img, lang in self._inputConfig.items():
            
            path = self.inFullPath(img)
            try:
                if not os.path.isfile(path):
                    raise exc.FileNotFoundError(img)

                text = OCR().imageToString(path=path, lang=lang)
                self.save(filename=img, text=text)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = App()
    app.main()
    Consensus(app.APP_CONFIG).create()