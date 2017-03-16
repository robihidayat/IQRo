#!/usr/bin/env python

# TODO : add file name

from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from os.path import basename
from glob import glob
from tqdm import tqdm
from lib.cleanshingregex import cleansing_regex as cr
from lib.cleanshinghmm import cleansing_entity as ce
from lib.stringmatching.cleanshing import filter_sampah, magic_number
from lib.fulltextsearch.fulltextsearch import fts_row_obat, fts_row_code, fts_row_toko, fts_row_jalan
from lib.stringmatching.string_match import ready_to_split
from lib.stringmatching.demarustringmatching import flag_demaru
from lib.stringmatching.demarustringmatching import flag_demaru_name_n_addres
from lib.treesearch.tree_search import query_string
from lib.treesearch.tree_search_apotek import query_apotek
import pandas as pd
import argparse
import signal
import sys

from lib.treesearch.tree_search_jalan import query_jalan

from lib.parse.parse_html import ParseTable
from lib.log import log
from lib.log.logflag import Logfile


if __name__ == '__main__':
    def exit_gracefully(signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, original_sigint)

        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)

        except KeyboardInterrupt:
            print("Ok ok, quitting")
            # ps.browser.quit()
            sys.exit(1)

            # restore the exit gracefully handler here
            signal.signal(signal.SIGINT, exit_gracefully)

    # store the original SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    # Parse Argument
    parser = argparse.ArgumentParser(description='Parse html table from abyy finereader result')
    parser.add_argument('folder', type=str,
                            help='folder of the file (.htm)')
    parser.add_argument('-o', '--output', type=str, default='result.tsv',
                            help='output of the file (.tsv)')
    parser.add_argument('-c', '--config', type=str, default='config.ini',
                            help='Configuration file that want to be load (.ini .cfg)')
    args = parser.parse_args()

    # read configuration files
    config = ConfigParser()
    config.read(args.config)
    nama_file_regex = config.get('Regex', 'file_name')
    ########################## MAIN PROGRAM ###########################

    files = glob(args.folder+'/*.htm')

    single_fields =["File Name"] + []
    column_fields = []
    sections = config.sections()
    for section in sections:
        option = config.options(section)
        if 'row' in option:
            single_fields.append(section)
        else:
            column_fields.append(section)
    fieldnames = ["File Name"] + single_fields + column_fields
    flag_file = open(args.output.replace('.tsv', '')+'_flag.tsv', 'wb')
    conf_file = open(args.output.replace('.tsv', '') + '_confident.tsv', 'wb')
    log_file = open(args.output.replace('.tsv', '') + '.log', 'wb')
    log_summary = open(args.output.replace('.tsv', '') + '_summary.log', 'wb')
    csvfile = open(args.output, 'wb')

    # Dummy OOP
    # ob_flag = Logfile('', pd.DataFrame(), log_file)

    ## Processing each file ##
    for idf, path_file in enumerate(tqdm(files)):

        # Parse and convert as json like
        # TODO: move it to ParseTable class as def parse to json
        # pprint.pprint(path_file)
        pt = ParseTable(path_file)
        cell = {}
        for field in single_fields:
            if field == fieldnames[0]:
                extra = {
                    field: basename(path_file)
                }
            else:
                try:
                    raw_result = pt.parsecell(config.getint(field, 'table'), config.getint(field, 'column'), config.getint(field, 'row')).encode('utf8')
                    # parse_raw = cleansing.gibberish(raw_result)
                    extra = {
                        field: raw_result
                    }
                except (NoOptionError, NoSectionError, IndexError):
                    extra = ""
            cell.update(extra)

        run_once = False
        results = [{}]
        tmp_results = [{}]
        for idy, field in enumerate(column_fields):
            # print field
            rows = ['']
            try:
                rows = pt.parsercolumn(config.getint(field, 'table'), config.getint(field, 'column'), config.getint(field, 'top_offset'), config.getint(field, 'bottom_offset'))
            except (IndexError, NoOptionError):
                pass

            if len(rows) is 0: rows += ['']
            if len(rows) >= len(results):
                results = [{} for i in range(len(rows))]

            for idx, row in enumerate(rows):
                raw_result = row.encode('utf8')
                # parse_raw = cleansing.gibberish(raw_result)
                extra = {field: raw_result}
                # result.update(extra)
                # result.update(cell)
                results[idx].update(extra)
                results[idx].update(cell)
                if run_once:
                    try:
                        results[idx].update(tmp_results[idx])
                    except IndexError:
                        pass
                        # sleep(3)
            run_once = True
            tmp_results = results
        df = pd.DataFrame(results)

        df['parsing'] = df['Product Description'].apply(lambda x: ce.cleansing_prodDesc(x))
        df['shop_input_fts'] = df['Shop Name']
        df['addres_input_fts'] = df['Shop Address']

        if config.has_section('Discount2'):
            df[['Date_bfr', 'Number_bfr', 'Name_bfr', 'Alamat_bfr', 'Price_bfr', 'Total_bfr', 'Diskon_bfr',
                'Diskon2_bfr', 'Unit_bfr']] = df[
                ['Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Price', 'Total Value', 'Discount',
                 'Discount2', 'Unit']]
        else:
            df[['Date_bfr', 'Number_bfr', 'Name_bfr', 'Alamat_bfr', 'Price_bfr', 'Total_bfr', 'Diskon_bfr', 'Unit_bfr']] = df[
                ['Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Price', 'Total Value','Discount', 'Unit']]
        ambil, bersih1, bersih2 = cr.regex_file(nama_file_regex)
        brutal = {}
        for column in df:
            purify = lambda x: x
            if column in 'File Name':
                purify = lambda x: x
            elif column in 'Price':
                purify = lambda x: cr.clean_price(x, 3, ambil, bersih1, bersih2)[0] if type(x) is str else None
            elif column in 'Total Value':
                purify = lambda x: cr.clean_price(x, 4, ambil, bersih1, bersih2)[0] if type(x) is str else None
            elif column in ['Discount', 'Discount2']:
                purify = lambda x: cr.clean_discount(x, ambil, bersih1, bersih2)[0] if type(x) is str else None
            elif column in 'Shop Name':
                purify = lambda x: fts_row_toko(query_apotek(cr.clean_shopname(x, ambil, bersih1, bersih2)[0])) if type(x) is str else None
            elif column in 'Shop Address':
                purify = lambda x: fts_row_jalan(query_jalan(cr.clean_address(x, ambil, bersih1, bersih2)[0])) if type(x) is str else None
            elif column in 'Invoice date':
                purify = lambda x: cr.clean_date(x, ambil, bersih1, bersih2)[0] if type(x) is str else None
            elif column in 'Invoice Number':
                purify = lambda x: cr.clean_invoice_number(x, ambil, bersih1, bersih2)[0] if type(x) is str else None
            elif column in 'Unit':
                purify = lambda x: cr.clean_unit(x, ambil, bersih1, bersih2)[0] if type(x) is str else None
            if column in 'Product Description':
                purify = lambda x: fts_row_obat(filter_sampah(magic_number(query_string(ready_to_split(ce.cleansing_prodDesc(x))))))
            brutal.update({
                column: df[column].map(purify).dropna().tolist()
            })
        df = df.from_dict({k: pd.Series(v) for k, v in brutal.iteritems()})
        cols_of_interest = ['Product Description', 'Unit', 'Price']
        df = df[(df[cols_of_interest]).any(axis=1)]
        df['Kode Obat'] = df['Product Description'].apply(lambda x: fts_row_code(x) if type(x) is str else None)
        dataa = []
        for index, row in df.iterrows():
            if row['Product Description'] != None:
                dataa.append(flag_demaru(row['Product Description'], row['parsing']))
        df['flag'] = dataa

        for index, row in df.iterrows():
            if row['flag'] == 'NOT CONFIDENT':
                row['Product Description'] = row['parsing']

        dataa = []
        for index, row in df.iterrows():
            if row['Shop Name'] != None:
                dataa.append(flag_demaru(row['Shop Name'], row['shop_input_fts']))
        df['Name_Flag'] = dataa

        for index, row in df.iterrows():
            if row['Name_Flag'] == 'NOT CONFIDENT':
                row['Shop Name'] = row['shop_input_fts']

        dataa = []
        for index, row in df.iterrows():
            if row['Shop Address'] != None:
                dataa.append(flag_demaru(row['Shop Address'], row['addres_input_fts']))
        df['Address_Flag'] = dataa

        for index, row in df.iterrows():
            if row['Address_Flag'] == 'NOT CONFIDENT':
                row['Shop Address'] = row['addres_input_fts']

        if config.has_section('Discount2'):
            df_flag = df[["File Name", 'parsing', 'Product Description', 'Kode Obat', 'flag', 'Price', 'Total Value', 'Discount',
                          'Discount2', 'Shop Name', 'Shop Address', 'Invoice date', 'Invoice Number', 'Unit']]
        else:
            df_flag = df[["File Name", 'parsing', 'Product Description', 'Kode Obat', 'flag', 'Price', 'Total Value', 'Discount',
                          'Shop Name', 'Shop Address', 'Invoice date', 'Invoice Number', 'Unit']]

        df_flag['Invoice_date_Flag'] = df['Date_bfr'].apply(
            lambda x: cr.clean_date(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        df_flag['Invoice_Number_Flag'] = df['Number_bfr'].apply(
            lambda x: cr.clean_invoice_number(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        df_flag['Price_Flag'] = df['Price_bfr'].apply(
            lambda x: cr.clean_price(x, 3, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        df_flag['Total_Value_Flag'] = df['Total_bfr'].apply(
            lambda x: cr.clean_price(x, 4, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        # df_flag['Name_Flag'] = df['Name_bfr'].apply(
        #     lambda x: cr.clean_shopname(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        # df_flag['Address_Flag'] = df['Alamat_bfr'].apply(
        #     lambda x: cr.clean_address(x, ambil, bersih2)[1] if type(x) is str else "NOT FOUND")
        df_flag['Name_Flag'] = df['Name_Flag']
        df_flag['Address_Flag'] = df['Address_Flag']
        if config.has_section('Discount2'):
            df_flag['Discount2_Flag'] = df['Diskon2_bfr'].apply(
                lambda x: cr.clean_discount(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
            df_flag['Discount_Flag'] = df['Diskon_bfr'].apply(
                lambda x: cr.clean_discount(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        else:
            df_flag['Discount_Flag'] = df['Diskon_bfr'].apply(
                lambda x: cr.clean_discount(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")
        df_flag['Unit_Flag'] = df['Unit_bfr'].apply(lambda x: cr.clean_unit(x, ambil, bersih1, bersih2)[1] if type(x) is str else "NOT FOUND")

        if config.has_section('Discount2'):
            df_Process = df[["File Name", 'Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Kode Obat', 'Product Description', 'Unit', 'Price', 'Discount', 'Discount2', 'Total Value']]
        else:
            df_Process = df[
                ["File Name", 'Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Kode Obat', 'Product Description', 'Unit', 'Price', 'Discount', 'Total Value']]
        if config.has_section('Discount2'):
            df_flag = df_flag[["File Name", 'Invoice date', 'Invoice_date_Flag', 'Invoice Number', 'Invoice_Number_Flag', 'Shop Name', 'Name_Flag', 'Shop Address', 'Address_Flag', 'Kode Obat', 'parsing', 'Product Description', 'flag', 'Unit', 'Unit_Flag', 'Price', 'Price_Flag', 'Discount','Discount_Flag',
                               'Discount2','Discount2_Flag', 'Total Value', 'Total_Value_Flag']]
        else:
            df_flag = df_flag[
                ["File Name", 'Invoice date', 'Invoice_date_Flag', 'Invoice Number', 'Invoice_Number_Flag', 'Shop Name', 'Name_Flag', 'Shop Address', 'Address_Flag', 'Kode Obat', 'parsing', 'Product Description', 'flag', 'Unit', 'Unit_Flag', 'Price', 'Price_Flag', 'Discount','Discount_Flag',
                 'Total Value', 'Total_Value_Flag']]

        df_Process = df_Process.set_index("File Name")
        df_Process = df_Process[df_Process['Product Description'] != 'NOT FOUND']

        ob_flag = Logfile(basename(path_file), df_flag, log_file) # Bad practice OOP
        log.log(basename(path_file), df_Process, log_file)
        ob_flag.log()

        df_flag = df_flag.set_index("File Name")
        df_conf = df_flag[df_flag['flag'] == 'CONFIDENT']
        df_flag = df_flag[df_flag['flag'] != 'NOT FOUND']
        if config.has_section('Discount2'):
            df_conf = df_conf[
                ['Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Kode Obat', 'Product Description', 'Unit', 'Price', 'Discount', 'Discount2',
                 'Total Value']]
        else:
            df_conf = df_conf[
                ['Invoice date', 'Invoice Number', 'Shop Name', 'Shop Address', 'Kode Obat', 'Product Description', 'Unit',
                 'Price', 'Discount', 'Total Value']]

        print_header = True if idf == 0 else False
        df_Process.to_csv(csvfile, mode='a', sep='\t', header=print_header)
        df_flag.to_csv(flag_file, mode='a', sep='\t', header=print_header)
        df_conf.to_csv(conf_file, mode='a', sep='\t', header=print_header)

        log_file.flush()
        conf_file.flush()
        csvfile.flush()
        flag_file.flush()

    log.log_summary(args.folder, log_summary)
    ob_flag.log_summary(log_summary)
