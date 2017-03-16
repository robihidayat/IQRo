import subprocess
from glob import glob
from pandas import DataFrame, read_csv
from datetime import datetime
import pandas as pd
import os


class Logfile:
    def __init__(self, file_name, df_out, log_output):
        self.file_name = file_name
        self.df_out = df_out
        self.log_output = log_output
        self.data_len = len(self.df_out.index)

        # TODO : make it to count all flag not just column 'flag'
        self.data_code_not_found = [row for row in self.df_out['flag'] if row == "CODE NOT FOUND"]
        self.data_not = [row for row in self.df_out['flag'] if row == "NOT FOUND"]
        self.data_word = [row for row in self.df_out['flag'] if row == "WORDS"]
        self.data_number = [row for row in self.df_out['flag'] if row == "NUMBERS"]
        self.data_confused = [row for row in self.df_out['flag'] if row == "NOT CONFIDENT"]
        self.data_yes = [row for row in self.df_out['flag'] if row == "CONFIDENT"]

        self.sum_code_not_found = 0
        self.sum_row = 0
        self.sum_not = 0
        self.sum_words = 0
        self.sum_number = 0
        self.sum_confused = 0
        self.sum_yes = 0


    def log(self):
        summery = self.get_stats()
        df = pd.DataFrame(summery.items())
        df.to_csv(self.log_output, mode='a', index=False, header=False)
        self._store(summery)


    def log_summary(self, log_output):
        summery = self.get_summary()
        df = pd.DataFrame(summery.items())
        df.to_csv(log_output, mode='a', index=False, header=False)


    def _store(self, sum_of_dict):
        self.sum_row += sum_of_dict['SUM ROW']
        self.sum_not += sum_of_dict['SUM NOT FOUND']
        self.sum_code_not_found += sum_of_dict['SUM CODE NOT FOUND']
        self.sum_words += sum_of_dict['SUM WORDS']
        self.sum_number += sum_of_dict['SUM NUMBERS']
        self.sum_confused += sum_of_dict['SUM NOT CONFIDENT']
        self.sum_yes += sum_of_dict['SUM CONFIDENT']


    def get_summary(self):
        return {
            "SUM ROW": self.sum_row,
            "SUM NOT FOUND": self.sum_not,
            "SUM CODE NOT FOUND": self.sum_code_not_found,
            "SUM WORDS": self.sum_words,
            "SUM NUMBERS": self.sum_number,
            "SUM NOT CONFIDENT": self.sum_confused,
            "SUM CONFIDENT": self.sum_yes
        }


    def get_stats(self):
        return {
            "SUM ROW": self.data_len,
            "SUM NOT FOUND": len(self.data_not),
            "SUM CODE NOT FOUND": len(self.data_code_not_found),
            "SUM WORDS": len(self.data_word),
            "SUM NUMBERS": len(self.data_number),
            "SUM NOT CONFIDENT": len(self.data_confused),
            "SUM CONFIDENT": len(self.data_yes)
        }


if __name__ == '__main__':
    pass
