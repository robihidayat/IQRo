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
import pandas as pd


def make_kamus_stopwords(files):
    dataframe_data = pd.read_csv(files, error_bad_lines=False, delimiter=',')
    return dataframe_data




