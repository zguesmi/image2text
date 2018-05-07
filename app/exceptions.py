import sys


class FatalError(Exception):

    message = 'Something went wrong ! Please Try Again'

    def __init__(self, message):
        sys.exit(message)


class NoConfigFileError(FatalError):

    message = 'No config file found - config.txt'

    def __init__(self):
        super().__init__(self.message)


class UnrespectedConfigFormatError(FatalError):

    message = 'Can not parse config file - required format is name:lang'

    def __init__(self):
        super().__init__(self.message)


class CustomError(Exception):

    def __init__(self, message):
        print(message)


class FileNotFoundError(CustomError):

    message = 'File not found - {}'

    def __init__(self, filename):
        super().__init__(self.message.format(filename))


class UnsupportedLanguageError(CustomError):

    message = 'Unsupported language - "{}"'

    def __init__(self, lang):
        super().__init__(self.message.format(lang))


class CanNotExtractTextError(CustomError):

    message = 'Can not extract text from image'

    def __init__(self):
        super().__init__(self.message)


class CanNotSaveTextError(CustomError):

    message = 'Can not write text to file'

    def __init__(self):
        super().__init__(self.message)