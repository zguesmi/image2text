module.exports = {
  name: 'image2text',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=ziedguesmi/image2text',
  },
  work: {
    cmdline: '',
    dirinuri: 'https://github.com/Zied-Guesmi/image2text/blob/master/DATADIR.zip?raw=true',
  }
};
