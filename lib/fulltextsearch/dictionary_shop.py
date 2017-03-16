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
import string

import pandas as pd
import re

a = lambda x: clean_shop(cleanshing_data(x))


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


def clean_shop(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    return regex.sub(' ', unicode(text, "utf-8").encode("ascii", "ignore"))


def make_kamus_shop(lokasi):
    dataframe_data = pd.read_csv(lokasi, error_bad_lines=False, delimiter=',')
    dataframe_data['shop_clean'] = dataframe_data['shop'].apply(a)
    dataframe_data['address_clean'] = dataframe_data['address'].apply(a)
    return dataframe_data




