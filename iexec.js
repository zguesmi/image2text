module.exports = {
  name: 'ocr-dapp',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=ziedguesmi/ocr',
  },
  work: {
    cmdline: 'python3 app.py',
  }
};
