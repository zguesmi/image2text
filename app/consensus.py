import os, sys, hashlib, yaml


class Consensus:

    def __init__(self):

        yml = yaml.load(open('app-config.yml'))
        self._out = '{}/{}/'.format( yml['datadir'], yml['output-dir'] )
        self._consensusFile = '{}/{}'.format(yml['datadir'], yml['consensus-file'])


    def fullPath(self, filename): return '{}{}'.format(self._out, filename)


    def create(self):

        md5 = hashlib.md5()

        try:
            consensus = open(self._consensusFile, 'w+')
        except Exception:
            sys.exit('can not create consensus file')

        for _file in os.listdir(self._out):
            
            path = self.fullPath(_file)
            try:
                with open(path, 'rb') as f:
                    buffer = f.read()
                    md5.update(buffer)
                consensus.write('{}\n'.format(md5.hexdigest()))
            except Exception:
                sys.exit('can not hash file {}'.format(path))
            
            
        