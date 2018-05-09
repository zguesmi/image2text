import pytesseract, cv2
import exceptions as exc



class OCR:

    LANGUAGES = {
        None: None,
        'en': 'eng',        # english
        'fr': 'fra',        # frensh
        'es': 'spa',        # Spanish
        'ar': 'ara',        # arabic
        'de': 'deu',        # German
        'zh': 'chi-sim',    # chinese
        'it': 'ita',        # Italian
        'ja': 'jpn',        # Japanese 
        'pt': 'por',        # Portuguese
        'ru': 'rus',        # russian
        'tr': 'tur',        # turkish
        'ko': 'kor'         # Korean
    }


    def _preprocess(self, image):
        
        ''' convert image to grayscale and apply threshold preprocessing '''
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    def _matchLanguage(self, lang):

        try:
            return self.LANGUAGES[lang]
        except KeyError:
            raise exc.UnsupportedLanguageError(lang)


    def imageToString(self, path, lang):

        image = self._preprocess(image=cv2.imread(path))

        try:
            return pytesseract.image_to_string(image, lang=self._matchLanguage(lang)).encode()
        except exc.UnsupportedLanguageError:
            raise
        except Exception as e:
            raise exc.CanNotExtractTextError(e, path)

