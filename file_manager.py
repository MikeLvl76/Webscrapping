class Manager:

    def __init__(self, filepath) -> None:
        self.file = filepath

    def get_file(self):
        return self.file

    def open_and_write(self, filename, encoding, text):
        with open(filename, 'w', encoding=encoding) as writer:
            writer.write(text)
    
    def open_and_read(self, filename, encoding):
        text = ''
        with open(filename, 'r', encoding=encoding) as reader:
            text = reader.readline()
        return text