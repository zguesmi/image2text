
<img src="./logo.png" width="400">


## Description
Ocr-dapp is an Ethereum ready dapp that applies [tesseract-OCR](https://github.com/tesseract-ocr/tesseract) to extract text from images.  

![demo](./images/demo.png)


## Usage
Put your images and your ```input-config.yml``` file in a folder (exp: DATADIR).The ```input-config.yml``` file defines language for each image and it should respect the ```<imagename>: <lang>``` format.

![screenshot](./images/screenshot-1.png)

Change datadir name in app-config.yml to the name of your folder (DATADIR for our example) and run the script.

    $ python3 app.py

You shoud find your text files in the ```DATADIR/out/``` folder

![screenshot](./images/screenshot-2.png)


## Supported languages
English (**en**), Spanish (**es**), Frensh (**fr**), Arabic (**ar**), German (**de**), Chinese simple (**zh**), Italian (**it**), Japanese (**ja**), Portuguese (**pt**), Russian (**ru**), Turkish (**tr**), Korean (**ko**).


## Supported image types
Tested extensions: **jpeg**, **bmp**, **png**  
Those extensions were not tested so they may not work properly: **pbm**, **pgm**, **ppm**, **tiff**, **rast**, **xbm**  

## Dependencies
[python3](https://www.python.org/)  
[tesseract-ocr](https://github.com/tesseract-ocr/tesseract)  
[opencv](https://opencv.org/)


## Docker installation

Install [docker](https://docs.docker.com/install/)

Prepare your datadir folder and grab the image from dockerhub

    $ docker run -v path/to/images/dir:/iexec/ ziedguesmi/ocr python app.py

Or you can build the image from dockerfile

    # clone the dapp
    $ git clone https://github.com/Zied-Guesmi/ocr-dapp.git && cd ocr-dapp/ 

    # build the docker image
    $ docker build -t ocr-dapp .

    # run the container
    $ docker run -v path/to/images/dir:/iexec/ ocr-dapp python3 app.py


## Installation
Install system dependencies:

    $ apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        libtesseract-dev \
        tesseract-ocr \
        tesseract-ocr-ara \
        tesseract-ocr-eng \
        tesseract-ocr-fra \
        tesseract-ocr-spa \
        tesseract-ocr-deu \
        tesseract-ocr-chi-sim \
        tesseract-ocr-ita \
        tesseract-ocr-jpn \
        tesseract-ocr-por \
        tesseract-ocr-rus \
        tesseract-ocr-tur \
        tesseract-ocr-kor
        
Install python depedencies:

    $ git clone https://github.com/Zied-Guesmi/ocr-dapp.git && cd ocr-dapp/app/
    $ pip3 install -r requirements.txt
