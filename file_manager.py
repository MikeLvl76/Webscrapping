import os

class Manager:

    def __init__(self, filepath, encoding) -> None:
        self.file = filepath
        self.encoding = encoding

    def get_file(self):
        return self.file

    # open and write in file (empty or not), enter a key and its value
    def write_attributes(self, key, value):
        lines = self.read_attributes()
        if len(lines) == 0:
            with open(self.file, 'w', encoding=self.encoding) as writer:
                writer.write(key + "=" + value)
        else:
            with open(self.file, 'a', encoding=self.encoding) as writer:
                writer.write("\n" + key + "=" + value)

    # open and write in file : select keys to remove, removed keys are replaced by empty char
    def remove_attributes(self, *keys):
        lines = self.read_attributes()
        if len(lines) > 0:
            with open(self.file, 'r+', encoding=self.encoding) as remover:
                for key in keys:
                    remover.seek(len(key) + 1, 0)
                
                print("SEEK\n" + remover.readline())
    
    # open and read file, return text as array of lines
    def open_and_read(self):
        with open(self.file, 'r', encoding=self.encoding) as reader:
            return reader.readlines()

    # read file split text on "=" symbol, return parts as a dict
    def read_attributes(self):
        dict = {}
        text = self.open_and_read()
        for t in text:
            key = t.split('=')[0]
            dict[key] = t.split('=')[1].replace("\n", "")
        return dict

if __name__ == "__main__":
    m = Manager(os.getcwd() + os.sep + "login.txt", 'utf-8')
    keys = m.read_attributes()
    print(keys)
    m.remove_attributes(list(keys)[0])