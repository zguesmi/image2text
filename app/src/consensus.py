import os, sys, hashlib, yaml
import exceptions as exc


class Consensus:


    def __init__(self, appConfigFile):

        yml = yaml.load(open(appConfigFile))
        self._datadir = yml['datadir']
        self._out = '{}/{}'.format( yml['datadir'], yml['output-dir'] )
        self._consensusFile = yml['consensus-file']


    def fullPath(self, filename):
        return '{}/{}'.format(self._datadir, filename)


    def outFullPath(self, filename):
        return '{}/{}'.format(self._out, filename)
   

    def hashFile(self, path):

        md5 = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                buffer = f.read()
                md5.update(buffer)
            return md5.hexdigest()
        except Exception as e:
            raise exc.FatalError(e)


    def create(self):

        try:
            consensus = open(self.fullPath(self._consensusFile), 'w+')

            for filename in os.listdir(self._out):

                path = self.outFullPath(filename)
                filehash = self.hashFile(path)
                consensus.write('{}\n'.format(filehash))

        except Exception as e:
            raise exc.FatalError(filename, e)
        finally:
            consensus.close()