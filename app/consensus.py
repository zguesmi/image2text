import os, sys, hashlib


class Consensus:


    IEXEC = '/iexec/'
    DATADIR = IEXEC + 'out/'
    CONSENSUS_FILE = IEXEC + 'consensus.iexec'


    def fullPath(self, filename):
        return '{}{}'.format(self.DATADIR, filename)


    def create(self):

        md5 = hashlib.md5()

        try:
            consensusFile = open(self.CONSENSUS_FILE, 'w+')
        except Exception:
            sys.exit('can not create consensus file')

        for _file in os.listdir(self.DATADIR):
            path = self.fullPath(_file)

            try:
                with open(path, 'rb') as f:
                    buffer = f.read()
                    md5.update(buffer)
                consensusFile.write('{}\n'.format(md5.hexdigest()))
            except Exception as e:
                sys.exit('can not hash file {}'.format(path))
            
            
        