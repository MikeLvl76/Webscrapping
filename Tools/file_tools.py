from os import sep, mkdir
from os.path import exists

# raised when unexpected behavior occurs
class FileException(Exception):

    def __init__(self, message) -> None:
        super().__init__(message)

# manages one file, some operations are available like create, read or append
# the file is contained in a directory, created if needed
class File_Manager:

    def __init__(self) -> None:
        self.file_path = ''
        self.dir_exists = False

    def get_file_path(self):
        return self.file_path

    def has_dir(self, dirname):
        self.dir_exists = exists(dirname)

    def create_file(self, dirname, file, extension, content):
        if self.dir_exists:
            mkdir(dirname)
            self.dir_exists = True
        self.file_path = f"../{dirname} + {sep} + {file}.{extension}"
        with open(self.file_path, 'w', encoding="utf-8") as writer:
            writer.write(content)

    def append_file(self, filepath, content = None):
        if not filepath:
            raise FileException('wrong path given')
        
        with open(filepath, 'a') as editor:
            if content is None:
                raise ValueError('no content to add in file')
            editor.write(content)

    def read_file(self, filepath):
        if not filepath:
            raise FileException('wrong path given')

        with open(filepath, 'r') as reader:
            return reader.readlines()