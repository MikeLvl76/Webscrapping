import os
import polars as pl
import sys

sys.tracebacklimit=0

PATH = os.getcwd() + os.sep

class ManagerException(Exception):
    def __init__(self, msg) -> None:
        super().__init__("Exception during process: " + msg)

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
    def get_col_list(self):
        return self.df.columns

    # open csv file and read given column name
    def read_cols(self, *cols) -> list:
        cols_read = []
        for arg in cols:
            cols_read = self.df[arg]
        return cols_read

    # open csv file and add column
    def add_cols(self, **cols) -> None:
        if len(cols) == 0: exit(0)
        names = self.read_cols(self.get_col_list())[0].columns
        for key in cols:
            if key in names: raise ManagerException(f'column "{key}" already inserted')
            self.df[key] = [cols.get(key)]
        self.df.to_csv(self.file, sep=";")

    # remove cols by name
    def remove_cols(self, cols = list) -> None:
        if len(cols) == 0: exit(0)
        names = self.read_cols(self.get_col_list())[0].columns
        for col in cols:
            if col not in names: raise ManagerException(f'column "{col}" cannot be deleted')
        self.df = self.df.drop(cols)
        self.df.to_csv(self.file, sep=";")

if __name__ == "__main__":
    m = Manager(PATH + "login.csv", 'utf-8')
    print(m.read_cols(m.get_col_list()))