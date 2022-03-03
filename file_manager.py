from msilib.schema import Error
import os
import polars as pl

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
    def read_cols(self, *cols) -> list[str]:
        cols_read = []
        for arg in cols:
            cols_read = self.df[arg]
        return cols_read[0].columns

    # open csv file and add column
    def add_cols(self, **cols) -> None:
        if len(cols) == 0: exit(0)
        names = self.read_cols(self.get_col_list())
        for key in cols:
            if key in names: raise ManagerException("column already inserted")
            self.df[key] = [cols.get(key)]
        self.df.to_csv(self.file, sep=";")

    def remove_cols(self, *cols) -> None:
        self.df = self.df.drop(cols)

if __name__ == "__main__":
    m = Manager(os.getcwd() + os.sep + "login.csv", 'utf-8')
    m.add_cols(**{"test" : 45435, "znfiesifviev" : 74535})
    print(m.read_cols(m.get_col_list()))