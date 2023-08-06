class File:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_bytes(self):
        with open(self.file_name, 'rb') as file:
            return file.read()