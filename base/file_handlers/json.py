class JSonFileHandler:
    file_path: str

    def __init__(self, file_path):
        self._file_path = file_path

    def parse_json(self) -> str:
        with open(self._file_path, 'r') as file:
            parsed_data = file.read()
        return parsed_data
