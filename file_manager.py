import os

class Manager:

    def __init__(self, filepath, encoding) -> None:
        self.file = filepath
        self.encoding = encoding

    def get_file(self):
        return self.file

    # open and write in file
    def open_and_write(self, text):
        with open(self.file, 'w', encoding=self.encoding) as writer:
            writer.write(text)
    
    # open and read file, return text as array of lines
    def open_and_read(self):
        text = ''
        with open(self.file, 'r', encoding=self.encoding) as reader:
            text = reader.readlines()
        return text

    # read file and return text of = symbol right side as array
    def read_attributes(self):
        l = []
        text = self.open_and_read()
        for t in text:
            l.append(t.split('=')[1].replace("\n", ""))
        return l


if __name__ == "__main__":
    m = Manager(os.getcwd() + os.sep + "login.txt", 'utf-8')
    print(m.read_attributes())