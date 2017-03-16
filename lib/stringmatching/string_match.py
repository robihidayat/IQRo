#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Modul ini mendemostrasikan penggunaan string macthing dengan menggunakan library difflib
dan database IMS yang telah di cleanshing. input kata yang akan dibandingkan akan di split
dan di compare dengan semua data yang ada di ims dengan data complementer. data complementer
adalah data tambahan yang tidak ada di ims.

Beberapa modul yang fucntion di modul ini adalah sebagai berikut:
    row_data()
    ratio()
    string_mathing()
    matchinging_apl()
    matchinging()
    matching_unit_keterangan()

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python string_mathing.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:

    row_data(): fucntion ini tidak mempunyai atribut. karena dikhususkan untk pemanggilan database ims.
        dan diiterasi perkata.

    ratio(string,string,float): function ini mempunyai tiga parameter. parameter pertama adalah string, sebagai variable kata yang akan di banding.
        parameter kedua juga string, sebagai variable kata pembanding. parameter terakhir adalah batas atau treshold untuk string matching.

    matchinging_apl(string): fucntion ini mempunyai satu parameter yaitu string.


Todo:
    * database kamus ims harus ada dalam database di mysql,dalam hal ini ada di localhost
    * database tersenut di cleanshing dan diiterasi per kata


Function Modul
==============
"""
import re
from cleanshing import simple_cleanshing
from lib.config_db.settingan import import_config_db

import MySQLdb as mdb
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])


'conect dengan database local'
"""
con : variable untuk mengakses database

parameter :
127.0.0.1 -> localhost, data mysql
root -> username db
root -> password db
factur_db -> database yang digunakan

variable tersebut disimpan ke dalam con, dan akan dipanggil untuk pemanggilan database dari mysql
"""
def row_data():
    """
apa aja harusnya kesisi
    """
    'sql syntax'
    sql = 'SELECT LOWER(pack_cleanshing) FROM Table_Medicine'
    try:
        'coba'
        with con:
            'cursor sql'
            cur = con.cursor()
            'execute sql'
            cur.execute(sql)
            'ambil hanya dalam row 0'
            cek = [row[0] for row in cur]
            return cek
    except:
        return ''


"""
new metode untuk split word but
"""


def get_number_digits(input_string):
    try:
        result = re.findall(r'(^[0-9]+[A-Za-z]+[0-9]+$)|(^[A-Za-z]+[0-9]+$)|(^[0-9]+[A-Za-z]+$)', input_string)
        return filter(None, result[0])[0]
    except:
        pass


def split_number_digits(input_string):
    try:
        return ' '.join(re.split('(\d+)',input_string))

    except:
        pass


def process_digits_number(input_string):
    data_string = []
    try:
        for rows in input_string.split():
            result = get_number_digits(rows)
            if result == None:
                data_string.append(rows)
            else:
                result_split = split_number_digits(result)
                data_string.append(result_split)
        result_string = ' '.join(data_string)
        return re.sub(' +',' ',result_string)
    except:
        pass


def ready_to_split(input_string):
    chek = []
    try:
        encoded_str = input_string.encode("utf8", "ignore")
        # print encoded_str,'inputs'
        proses_string = simple_cleanshing(encoded_str)
        split_string = proses_string.split()
        # print split_string , 'mbuh'
        kata_process = ' '.join(split_string)
        chek.append(process_digits_number(kata_process))
        if chek[0] == None:
            return kata_process
        else:
            return process_digits_number(kata_process)

    except:
        pass

