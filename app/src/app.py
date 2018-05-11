import os, sys, subprocess, imghdr, yaml

import exceptions as exc
from consensus import Consensus
from ocr import OCR



class App:

    APP_CONFIG_FILE = '../app-config.yml'
    _SUPPORTED_IMAGES = [ 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png' ]

    _taskStartedFlag = '-> processing file {}'
    _taskEndedFlag = 'done..'
    _executionEndedFlag = 'Supported images have been moved to "{}" folder. Text files have been saved in "{}" folder.'


    def __init__(self):

        yml = yaml.load(open(self.APP_CONFIG_FILE))

        self._datadir = yml['datadir']
        self._inputConfigFile = '{}/{}'.format( yml['datadir'], yml['input-config'] )
        self._in = '{}/{}'.format( yml['datadir'], yml['input-dir'] )
        self._out = '{}/{}'.format( yml['datadir'], yml['output-dir'] )
        self._outputFileExtension = yml['output-files-extension']
        self._executionEndedFlag = self._executionEndedFlag.format( yml['input-dir'], yml['output-dir'] )

        self._inputConfig = self.parseConfigFile()

        self.prepareDatadir()


    def fullPath(self, filename):
        return '{}/{}'.format( self._datadir, filename )


    def inFullPath(self, filename):
        return '{}/{}'.format( self._in, filename )


    def outFullPath(self, filename):
        return '{}/{}.{}'.format( self._out, filename, self._outputFileExtension )


    def isNotConfigFile(self, filename):
        return self.fullPath(filename) != self._inputConfigFile


    def isSupportedImage(self, filename):
        return ( os.path.isfile(self.fullPath(filename))
            and imghdr.what( self.fullPath(filename) ) in self._SUPPORTED_IMAGES
            and self.isNotConfigFile(filename) )


    def parseConfigFile(self):

        if not os.path.isfile(self._inputConfigFile):
            raise exc.ConfigFileNotFoundError(self._inputConfigFile)

        try:
            return yaml.load(open(self._inputConfigFile))
        except Exception as e:
            raise exc.UnrespectedConfigFormatError(e)


    def prepareDatadir(self):
    
        try:
            os.mkdir(self._in)

            for f in [ f for f in os.listdir(self._datadir) if self.isSupportedImage(f) ]:
                subprocess.call([ 'mv', self.fullPath(f), self._in ])

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

            try:

                print(self._taskStartedFlag.format(img))
                path = self.inFullPath(img)

                if not os.path.isfile(path):

                    if os.path.isfile(self.fullPath(img)):
                        raise exc.FileTypeNotSupportedError(img)

                    raise exc.FileNotFoundError(img)
                
                text = OCR().imageToString(path=path, lang=lang)
                self.save(filename=img, text=text)
                
                print(self._taskEndedFlag)

            except exc.CustomError:
                pass
            except Exception as e:
                print(e)

        print(self._executionEndedFlag)

if __name__ == '__main__':
    app = App()
    app.main()
    Consensus(app.APP_CONFIG_FILE).create()