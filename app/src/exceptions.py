import sys, yaml


class FatalError(Exception):

    def __init__(self, message):
        sys.exit(message)


class ConfigFileNotFoundError(FatalError):

    message = 'Input config file not found - {}'

    def __init__(self, filename):
        super().__init__(self.message.format(filename))


class UnrespectedConfigFormatError(FatalError):

    message = 'Error parsing input config file - required format is name:lang\n{}'

    def __init__(self, err):
        super().__init__(self.message.format(err))


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

    message = 'Error extracting text from image - {}\n{}'

    def __init__(self, err, filename):
        super().__init__(self.message.format(filename, err))


class CanNotSaveTextError(CustomError):

    message = 'Error writing text to file - {}\n{}'

    def __init__(self, err, filename):
        super().__init__(self.message.format(filename, err))


class CanNotCreateConsensusFile(FatalError):

    message = 'Error creating consensus file - {}\n{}'

    def __init__(self, err, filename):
        super().__init__(self.message.format(filename, err))