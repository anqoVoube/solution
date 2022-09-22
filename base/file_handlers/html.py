class HTMLFileHandler:
    """
    Creates html file with given text

    Attrs:
        `file_path`: Path of html file to be created.
        `text`: Text to be added in created html file.
    """
    file_path: str
    text: str

    def __init__(self, file_path, text):
        self._file_path = file_path
        self.text = text

    def create(self):
        with open(self._file_path, 'a+') as file:
            file.write(self.text)