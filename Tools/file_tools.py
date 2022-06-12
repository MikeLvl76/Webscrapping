from os import getcwd, sep, mkdir
from os.path import exists, abspath
import pandas as pd

# raised when unexpected behavior occurs
class FileException(Exception):

    def __init__(self, message) -> None:
        super().__init__(message)

# manages one file, some operations are available like create, read or append
# the file is contained in a directory, created if needed
class File_Manager:

    def __init__(self) -> None:
        self.file_path = ''

    def find_file(self, base, dirname, file):
        if not exists(base + sep + dirname + sep + file):
            return None
        self.file_path = abspath(base + sep + dirname + sep + file)

    def get_file_path(self):
        return self.file_path

    def create_file(self, dirname, file, extension, content):
        if not exists(dirname):
            mkdir(dirname)
        self.file_path = "{}{}{}.{}".format(dirname, sep, file, extension)
        with open(self.file_path, 'w', encoding="utf-8") as writer:
            writer.write(content)
        print(f"File created at path : {self.file_path}")

    def append_file(self, filepath, pandas=False, **content):
        if not filepath:
            raise FileException('wrong path given')
        
        if not pandas:
            with open(filepath, 'a') as editor:
                editor.write(content)
        df = self.read_file(filepath, pandas=True)
        print(df)
        for keys, values in content.items():
            print(values)
            df[keys] = values
        df.to_csv(self.file_path)
        print(f"File appended at path : {self.file_path}")

    def read_file(self, filepath, *cols, pandas=False):
        if not filepath:
            raise FileException('wrong path given')

        print(f"Reading file at path : {self.file_path}...")
        if not pandas:
            with open(filepath, 'r') as reader:
                return reader.readlines()
        return pd.read_csv(self.file_path).loc[:,cols] if len(cols) > 0 else pd.read_csv(self.file_path)

manager = File_Manager()
manager.find_file(getcwd(), 'results', 'election.csv')
manager.append_file(manager.get_file_path(), True, test=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
print(manager.read_file(manager.get_file_path(), 'candidats', 'partis', pandas=True))