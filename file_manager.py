import os
import polars as pl

class Manager:

    def __init__(self, filepath, encoding) -> None:
        assert filepath.find(".csv") != -1, "not a csv file"
        self.file = filepath
        self.encoding = encoding
        self.df = pl.read_csv(self.file, sep=';',
                         ignore_errors=True, low_memory=True)

    def get_file(self) -> str:
        return self.file  

    # open csv file and retrieve columns
    def get_collist(self):
        return self.df.columns

    # open csv file and read given column name
    def read_cols(self, *args) -> list:
        args_read = []
        for arg in args:
            args_read = self.df[arg]
        return args_read

    # open csv file and add column
    def add_cols(self, **args):
        if len(args) == 0: exit(0)
        for key in args:
            self.df[key] = args.get(key)

if __name__ == "__main__":
    m = Manager(os.getcwd() + os.sep + "login.csv", 'utf-8')
    m.add_cols(**{"test" : 45435, "znfiesifviev" : 74535})
    print(m.read_cols(m.get_collist()))