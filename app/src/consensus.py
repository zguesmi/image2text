import os, sys, hashlib, yaml


class Consensus:

    def __init__(self, appConfig):

        yml = yaml.load(open(appConfig))
        self._out = '{}/{}'.format( yml['datadir'], yml['output-dir'] )
        self._consensusFile = '{}/{}'.format(yml['datadir'], yml['consensus-file'])


    def fullPath(self, filename):
        return '{}/{}'.format(self._out, filename)


    def create(self):

        consensus = openFile(self._consensusFile)

        for filename in os.listdir(self._out):

            path = self.fullPath(filename)
            filehash = hashFile(path)
            try:
                consensus.write('{}\n'.format(filehash))
            except Exception:
                sys.exit('can not hash file {}'.format(path))
            finally:
                consensus.close()


def openFile(path):
    try:
        return open(path, 'w+')
    except Exception:
        sys.exit('can not create consensus file')
    


def hashFile(path):

    md5 = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            buffer = f.read()
            md5.update(buffer)
        return md5.hexdigest()
    except Exception:
        pass
