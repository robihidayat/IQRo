# -*- coding: utf-8 -*-
""" Google style docstrings

Modul yang berisi kumpulan fucntion yang berisi simple cleanshing, remove_barang,remove_number,clean_shop,magic_number.
inti dari modul ini adalah sebagai modul cleanshing data input.

File name: dictionary.py
Author: Robi Hidayat
Date created: 6/12/2016
Date last modified: 6/02/2017
Python Version: 2.7

"""
import re


def simple_cleanshing(input_string):
    """ Function with types documented in the docstring.

    Function ini adalah untuk membuat data input menjadi normal (function untuk menghilangkan simbols dan memisahkan antara huruf dan angka).
    cleanshing yang dilakuka adalah menghilangkan simbol dan memisahkan kata dengan
    digits.

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """
    # input_string = input_string.encode('utf-8', 'ignore')
    # jadikan sebagai string
    str_input = str(input_string)
    # input string, dan hilangankan selain symbols
    str_filter_non_words = re.sub(r'[^\w]', ' ', str_input)
    # Jadikan lowercase
    # menghilangkan non words
    str_filter_non_words_lower = str_filter_non_words.lower()
    # lupa, pokoknya menghilangkan bagian yang gak diperlukan
    # lowercase
    pattren_regex = u"[^\{}-]+"
    # lupa
    find_string = re.findall(pattren_regex, str_filter_non_words_lower)
    # join dari hasil regex, karena hasilnya di split
    # di join, karena hasil dari findll adalah dalam bentuk list
    filter_join = ''.join(find_string)
    # pisahkan digits dan non digits
    # joinkan lagi
    # lol = ' '.join(lol)
    # hilangkan
    filter_join = filter_join.replace('/',' ')
    # joinkan lagi
    filter_join = ' '.join(filter_join.split())
    # return if none adalah kosong
    if filter_join == None:
        row =''
    # else return dalam bentuk clean, dgits dan words
    return filter_join


def remove_barang(input_string):

    """ Function with types documented in the docstring.

    Function ini adalah untuk membuat data input menjadi normal.
    function yang digunakan untuk menghilangkan row yang hanya mengandung keterangan saja.

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """

    try:
        # variable stopwords
        stopwords = ['nama','barang','jkn']
        # variable keterangan
        keterangan = ['tablet','cream','krim','tab','syrup']
        # gabungan dari kedua variable
        stopwords_tabs = stopwords + keterangan
        # split inputan dari parameter'
        input_string_split = input_string.lower().split()
        # cari tau berapa kata yang masuk
        len_string = len(input_string_split)
        # jika itu kurang dari 3 suku kata maka:
        if len_string <= 1:
            # hilangkan kata yang mengandung kedua variable kata tersebut
            list_kata = [row for row in input_string_split if row not in stopwords_tabs]
            # joinkan kembali
            kata_join = ' '.join(list_kata)
            # hilangkan jika itu bukan angka
            filter_kata = ''.join([row for row in kata_join if not row.isdigit()])
            # hilangkan apostpoe
            filter_kata = filter_kata.replace("'", "")
            # retrunkan kembali
            return filter_kata

            # else, jika lebih dari 4 suku kata
        elif len_string >= 2:
            # hilangkan kata yang mengandung kata di variable stopwords
            list_kata_min = [row for row in input_string_split if row not in stopwords]
            # joinkan lagi
            kata_max =  ' '.join(list_kata_min)
            # hilangkan apostope
            kata_filter = kata_max.replace("'", "")
            # retun kata
            return kata_filter
    except:
        pass


def remove_number(input_string):

    """ Function with types documented in the docstring.

    Function ini adalah untuk membuat data input menjadi normal.
    cleanshing yang dilakuka adalah function yang hanya menghilangkan nomer


    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """

    try:
        # bila ada digits maka hilangkan'
        filter_number = ''.join([row for row in input_string if not row.isdigit()])
        # return digits only'
        return filter_number
    except:
        # pass jika err'
        pass


def clean_shop(input_string):
    """ Function with types documented in the docstring.

    Function ini adalah untuk membuat data input menjadi normal.
    cleanshing yang dilakuka adalah function function akan menghilankan kata yang ada di
    stopwords dalam hal ini adalah untuk nama shop


    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """
    stopwords = ['dikirim']
    # pisahkan huruf dan angka
    kata_clean = simple_cleanshing(input_string)
    # hilangkan keterangan
    kata_remove_shop = ' '.join([row for row in kata_clean.split() if row not in stopwords])
    # return dan di uppwercase
    return kata_remove_shop.upper()


def magic_number(input_string):

    """ Function with types documented in the docstring.

    Function ini adalah untuk mentrasnpose data inputan bila ada input kata yang kurang dari sama dengan 3 atau digits
    maka akan pindah ke belakang.

    Example :
        Input -> 12 ML Panadol
        Output -> Panadol 12 ML

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi
    """

    try:
        # set found as True boolean
        found = True
        # set counter_x as 1
        counter_x=1
        # logical function, if all data is digits then remove
        if all(item.isdigit() for item in input_string.split()) == True:
            return ''
        # or if input element 1 adalah bukan digits
        elif not input_string.split()[0].isdigit():
            # retrun input
            return input_string
        # split
        lists_split = input_string.split()
        # if row in list lebih dari 3
        lists_split = [row for row in lists_split if len(row) >=3]
        # do while true
        while found == True:
            # transpose
            lists_split = lists_split[x:] + lists_split[:x]
            # if tidak ada element di 1st.
            if not lists_split[0].isdigit() :
                # set found = False
                found = False
                # count
                counter_x +=1
        # print ' '.join(lists_split)
        return ' '.join(lists_split)

    except:
        pass


def itung_len(input_string):

    """ Function with types documented in the docstring.

    function untuk menghitung len data di setiap element

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi


    """
    len_list = []
    try:
        string_list = input_string.split()
        len_list = [len(row) for row in string_list]
        return len_list
    except:
        pass


def limit_sampah(items):
    """ Function with types documented in the docstring.

    function for limit len element

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi


    """

    return all(i <= 3 for i in items)


def filter_sampah(input_string):

    """ Function with types documented in the docstring.

    function for filltering sampah

    Args:
        input_string (str) : Paramater pertama


    Returns:
        string : return valuenya adalah string yang sudah dinormalisasi


    """

    try:
        len_list = itung_len(input_string)
        if limit_sampah(len_list) == True:
            return ''
        else:
            return input_string

    except:
        pass
