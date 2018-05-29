import os
import sys
import subprocess

import imghdr
import yaml
import yamlordereddictloader

import custom_exceptions as customExceptions
from consensus import Consensus
from ocr import OCR


class Flag:

    taskStarted = '[INFO] processing file {}'
    taskEnded = '[INFO] done..\n'
    executionEnded = '[INFO] Text files have been moved to "{}" folder.\n' \
                   + '[INFO] Sound files are saved in "{}" folder.'

class App:

    _SUPPORTED_IMAGES = [ 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png' ]
    _PREFIX = 'original'
    _EXTENSION = '.txt'
    _appConfigFile = '{}/app-config.yml'

    def __init__(self):
        self._paths = {}
        self.flag = Flag()
        self.readAppConfigFile()
        self.readInputConfigFile()
        self.prepareDatadir()


    @property
    def datadir(self):
        return self._paths['/']


    @property
    def out(self):
        return self._paths['/out']


    def readAppConfigFile(self):
        dirname = os.path.dirname
        path = self._appConfigFile.format(dirname(dirname(os.path.realpath(__file__))))
        if not os.path.isfile(path):
            raise customExceptions.AppConfigNotFoundError(path)
        try:
            yml = yaml.load(open(path), yamlordereddictloader.SafeLoader)
            self._paths['/'] = yml['datadir']
            self._paths['/in'] = '{}/{}'.format(yml['datadir'], yml['input-dir'])
            self._paths['/out'] = '{}/{}'.format(yml['datadir'], yml['output-dir'])
            self._paths['conf'] = '{}/{}'.format(yml['datadir'], yml['input-config'])
            self.flag.executionEnded = self.flag.executionEnded.format(yml['input-dir'], yml['output-dir'])
        except Exception as e:
            raise customExceptions.IllegalAppConfigFormatError(e)

    def readInputConfigFile(self):
        if not os.path.isfile(self._paths['conf']):
            raise customExceptions.InputConfigNotFoundError(self._paths['conf'])
        try:
            self._inputConfig = yaml.load(open(self._paths['conf']), yamlordereddictloader.SafeLoader)
        except Exception as e:
            raise customExceptions.IllegalInputConfigFormatError(e)

    def getAbsPath(self, dirname, filename, extension=''):
        return '{}/{}{}'.format(self._paths[dirname], filename, extension)

    def isNotConfigFile(self, filename):
        return self.getAbsPath('/', filename) != self._paths['conf']

    def isSupportedImageType(self, filename):
        return ( os.path.isfile(self.getAbsPath('/', filename)) and
            self.isNotConfigFile(filename) and
            imghdr.what( self.getAbsPath('/', filename) ) in self._SUPPORTED_IMAGES )

    def prepareDatadir(self):
        try:
            datadirContent = os.listdir(self._paths['/'])
            os.mkdir(self._paths['/in'])
            os.mkdir(self._paths['/out'])
            for filename in [ f for f in datadirContent if self.isSupportedImageType(f) ]:
                subprocess.call([ 'mv', self.getAbsPath('/', filename), self._paths['/in'] ])
        except Exception as e:
            raise customExceptions.FatalError(e)

    def save(self, filename, text):
        try:
            path = self.getAbsPath('/out', filename, self._EXTENSION)
            fp = open(path, 'wb')
            fp.write(text)
        except Exception as e:
            raise customExceptions.CanNotSaveTextError(e, path)
        finally:
            fp.close()
    
    def renameInputFiles(self):
        for filename in os.listdir(self._paths['/in']):
            oldPath = self.getAbsPath('/in', filename)
            newName = '{}-{}'.format(self._PREFIX, filename)
            newPath = self.getAbsPath('/in', newName)
            subprocess.call([ 'mv', oldPath, newPath ])


    def main(self):

        for img, lang in self._inputConfig.items():
            try:
                print(self.flag.taskStarted.format(img))
                filepath = self.getAbsPath('/in', img)

                if not os.path.isfile(filepath):
                    if os.path.isfile(self.getAbsPath('/', img)):
                        raise customExceptions.FileTypeNotSupportedError(filepath)
                    raise customExceptions.FileNotFoundError(filepath)

                text = OCR().imageToString(path=filepath, lang=lang)
                self.save(filename=img, text=text)
                print(self.flag.taskEnded)
            except customExceptions.CustomError:
                pass
            except Exception as e:
                print(e)

        self.renameInputFiles()
        print(self.flag.executionEnded)


if __name__ == '__main__':
    app = App()
    app.main()
    Consensus(datadir=app.datadir, outputdir=app.out)