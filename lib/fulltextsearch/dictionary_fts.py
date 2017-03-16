# -*- coding: utf-8 -*-
""" Google style docstrings

Modul ini adalah sebuah dokumen yang membuat kamus ims menjadi standar dan
sesuai dengan format yang telah disesuaikan. Dikarenakan hasil dari kamus ims
tidak sesuai, sebagai contoh.

Example:
    PANADOL 12ML/39GR --> PANADOL 12 ML 39 GR GRAM GRAMS

Data tersebut akan disimpan dalam database sql, agar bisa di index oleh fts.
format data yang dibuat adalah sebagai berikut:

| Pack | pack_cleanshing | Code_Obat


|PANADOL 12ML/39GR | PANADOL 12 ML 39 GR GRAM GRAMS | 32910


Attributes:


Todo:
    * untuk menggunakan modul ini, mysql harus terinstall dan enngie yang digunakan adalah myiisam
    * file yang akan diolah adalah csv


File name: dictionary.py
Author: Robi Hidayat
Date created: 6/12/2016
Date last modified: 6/02/2017
Python Version: 2.7


"""
# import MySQLdb as mdb
import pandas as pd
import re

a = lambda x: duplicate_del(x)
b = lambda x: alias_kamus(x, reps)

"""
str: Module level variable documented inline

a adalah variable string untuk memanggil fungsi duplicate_del
b adalah variable string untuk memanggil fungsi alias_kamus


"""
# con = mdb.connect('127.0.0.1', 'bawendb', 'langensari', 'facture_db');

# con = mdb.connect('127.0.0.1', 'root', '', 'test')
"""str: Module level variable documented inline
# file server
# con = mdb.connect('192.168.101.74', 'bawendb', 'langensari', 'facture_db');
con adalah string variable modul untuk dapat menggunakan database mysql.

Attributes:
    con = mdb.connect(str[1], str[2], str[3], str[3]);
    str[1] -> ip addres mysql server
    str[2] -> useer
    str[3] -> pass
    str[4] -> database

"""

reps = {'TABLET': 'TAB TABELLA',
        'TAB': 'TABLET',
        'SYR': 'SYRUP SIRUP',
        'CAP': 'CAPLET CAPSULE',
        'DRY': 'DRAY',
        'RESPULES': 'RESP',
        'AMP': 'AMPULLA AMPULE AMPUL AMPOULE',
        'AQ': 'AQUA WATER',
        'CER': 'CERA WAX',
        'COLLUT': 'COLLUTORIM MOUTHWASH',
        'COLLYR': 'COLLYRIUM EYEWASH',
        'DECOCT': 'DECOCTUM DECOCTION',
        'EMULS': 'EMULSUM EMULSION',
        'LIQ': 'LIQUOR SOLUTION',
        'MIXT': 'MIXTURA MIXTURE',
        'OCULENT': 'OCULENTUM OINTMENT',
        'PALV ADSP': 'ADSP PALVIS ADSPERSORIUS SPRINKLED POWDER',
        'LOT': 'LOTION',
        'EXPECT': 'EXPECTORANT',
        'OBHC': 'OBH COMBI'
        }

""" Dick: variable untuk mendefinisikan file nama obat yang akan di normalisasi
reps adalah variable dengan tipe data dict yang sebagai penyimpanan kata yang
akan di tambahkan ke dalam database kamus ims.

Attributes:
    reps = {key(str):value(str)}

"""


def cleanshing_data(input_string):

    """ Function with types documented in the docstring.

    Function ini adalah untuk membuat data input menjadi normal.
    cleanshing yang dilakuka adalah menghilangkan simbol dan memisahkan kata dengan
    digits.

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """

    pattern_regex = u"[^\{}-]+"
    # pattern regex
    get_string = re.findall(pattern_regex, input_string)
    # proses regex filltering
    data_string = ' '.join(get_string)
    # join string
    string_process = re.split('(\d+)',data_string)
    # split digits and words
    string_process = ' '.join(string_process)
    # join string
    strs_final = string_process.replace('/',' ')
    # replace simbol '/'
    strs_final = ' '.join(strs_final.split())
    # join adn retrun
    return strs_final


def duplicate_del(input_string):

    """ Function with types documented in the docstring

    Function ini adalah untuk menghilangkan string yang double.

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string tidak double

    """
    return ' '.join(list(set(input_string.split())))


def alias_kamus(text, dic):
    """ Function with types documented in the docstring

    Function untuk menambahkan data string jika ada pada key yang sama dengan di kamus.

    Args:
        text (str) : Paramater pertama
        dic (dict) : Parameter kedua

    Returns:
        string : data dengan penambahan kata

    """

    clean_type = cleanshing_data(text)
    string_process = ' '.join([value for key, value in dic.iteritems() if key in text.split()])
    if not string_process:
        return text+' '+clean_type
    else:
        return string_process+' '+text+' '+clean_type


def make_kamus_medicine(lokasi):
    dataframe_data = pd.read_csv(lokasi, error_bad_lines=False, delimiter=',')
    dataframe_data[['pack_cleanshing']] = dataframe_data[['Pack']]
    dataframe_data['pack_cleanshing'] = dataframe_data['pack_cleanshing'].apply(b)
    dataframe_data['pack_cleanshing'] = dataframe_data['pack_cleanshing'].apply(a)
    return dataframe_data





