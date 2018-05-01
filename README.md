# OCR-Dapp

![dapp logo](./logo.png)


## Description
This dapp applies [tesseract-OCR](https://github.com/tesseract-ocr/tesseract) on a given image and extracts text from it.  

## Usage
    # Help
    $ python3 ocr.py -h

    # Apply threshold preprocessing and extract text
    $ python3 ocr.py -i path/to/image -l en -p thresh 

## Supported languages
English (en), Spanish (es), Frensh (fr), Arabic (ar), German (de), Chinese simple (zh), Italian (it), Japanese (ja), Portuguese (pt), Russian (ru), Turkish (tr), Korean (ko).

## Dependencies
[python3](https://www.python.org/)  
[tesseract-ocr](https://github.com/tesseract-ocr/tesseract)  
[opencv](https://opencv.org/)

## Docker installation
Install [docker](https://docs.docker.com/install/)

    $ docker run -v .:/app ziedguesmi/ocr -i path/to/image -l en -p thresh

or

    # clone the dapp
    $ git clone https://github.com/Zied-Guesmi/ocr-dapp.git

    # build the docker image
    $ cd ocr-dapp/
    $ docker build -t ocr-dapp .

    # run the docker container
    $ docker run -v .:/app/ ocr-dapp -i path/to/image -l en -p thresh

    $ cat out.txt

## Native installation
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

    $ git clone https://github.com/Zied-Guesmi/ocr-dapp.git
    $ cd ocr-dapp/app/
    $ pip3 install -r requirements.txt