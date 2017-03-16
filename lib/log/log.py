import subprocess
from glob import glob
from pandas import DataFrame, read_csv, Series
from datetime import datetime
import os

result_file = 'output.tsv'
input_file = 'APL'
config_file = 'APL.ini'
log_file = 'log.tsv'
cmd = 'python bulk_parse_table.py -o '+result_file+'-c '+config_file+' '+input_file

_index = 0
def log(file_name, df_out, log_output):
    global _index
    dict_temp = {
        '-----------'   : '------------',
        'No'            : _index,
        'Processed File': file_name,
        'Writen At'     : datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    }
    # print len(df_flag['flag'] == 'NOT FOUND')

    # try:
    #     df_log = read_csv(log_file)
    # except IOError:
    #     res_dir, res_file = os.path.split(os.path.abspath(log_file))
    #     try:
    #         os.makedirs(res_dir)
    #     except:
    #         pass
    #     df_log = DataFrame()
    # print df_out
    # df_log = df_log.from_dict({k: Series(v) for k, v in dict_temp.iteritems()})
    df_log = DataFrame(dict_temp.items())
    df_log.to_csv(log_output, mode='a', index=False, header=False)
    _index += 1

    # print df_out[df_out['flag'] == 'NUMBERS']

def log_summary(folder_name, log_output):
    dict_temp = {
        'Total File': _index,
        'Processed Folder': folder_name,
        'Writen At': datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    }

    df_log = DataFrame(dict_temp.items())
    df_log.to_csv(log_output, mode='a', index=False, header=False)


if __name__ == '__main__':
    # log process
    # df_out = read_csv(result_file, sep='\t')
    # try:
    #     df_log = read_csv(log_file)
    # except IOError:
    #     res_dir, res_file = os.path.split(os.path.abspath(log_file))
    #     os.makedirs(res_dir)
    #     os.mknod(res_file)
    #     df_log = read_csv(log_file)
    #
    # list_files = glob(input_file)
    # ## log output processed file
    # #input-output
    # diff_file = df_out['File_Name'].tolist()-list_files
    # df_log['Processed_File'] = df_out['File_Name']
    # ## log count output row
    # ## log start&end process
    # subprocess.call(cmd)
    pass
