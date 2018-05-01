module.exports = {
  name: 'ocr-dapp',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=docker-image-name',
  },
  work: {
    cmdline: 'cli arguments',
  }
};
