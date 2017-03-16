import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import string

def regex_file(nama_file):
    regex = pd.ExcelFile(nama_file)
    ambil = regex.parse("Regex")
    bersih1 = regex.parse("Clean_awal")
    bersih2 = regex.parse("Clean_akhir")
    return ambil, bersih1, bersih2

def clean_invoice_number(item, ambil, bersih1, bersih2):
    akhir1 = bersih1["Invoice Number"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Invoice Number"].dropna()
    n = 0
    while n < len(list_regex):
        hasil = re.findall(str(list_regex[n]), str(item))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Invoice Number"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    if len(hasil) == 0:
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_date(item, ambil, bersih1, bersih2):
    akhir1 = bersih1["Invoice Date"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Invoice Date"].dropna()
    n = 0
    while n < len(list_regex):
        hasil = re.findall(str(list_regex[n]), str(item))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Invoice Date"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    if len(hasil) == 0:
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_discount(item, ambil, bersih1, bersih2):
    akhir1 = bersih1["Discount"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Discount"].dropna()
    n = 0
    while n < len(list_regex):
        hasil = re.findall(str(list_regex[n]), str(item))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Discount"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    if len(hasil) == 0:
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_shopname(item, ambil, bersih1, bersih2):
    def filtera(item, max_number):
        if len(item) > max_number:
            x = item
        else:
            x = ''
        return x

    akhir1 = bersih1["Shop Name"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Shop Name"].dropna()
    n = 0

    while n < len(list_regex):
        hasil = re.findall(str(list_regex[n]), str(item))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Shop Name"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    hasil = re.sub(r'\.', ' ', str(hasil))
    hasil = re.sub(r'\s+', ' ', str(hasil))
    hasil = filtera(hasil, 5)
    if len(hasil) == 0:
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_address(item, ambil, bersih1, bersih2):
    def filtera(item, max_number):
        if len(item) > max_number:
            x = item
        else:
            x = ''
        return x

    item = re.sub(r'[^\x00-\x7F]+', '', str(item))

    akhir1 = bersih1["Shop Address"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Shop Address"].dropna()
    n = 0
    while n < len(list_regex):
        hasil = re.findall(str(list_regex[n]), str(item))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Shop Address"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    hasil = re.sub(r'\.', ' ', str(hasil))
    hasil = re.sub(r'\s+', ' ', str(hasil))
    hasil = re.sub(r'(?:PO|SO|FO|fO|pO|po|RO|PQ)\s(?:DUE|Due|Dua|Dve|DVE|D[U|u]|Oue|Dv|Qua)', '', str(hasil))
    hasil = filtera(hasil, 4)
    if len(hasil) == 0:
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_price(item, max_char, ambil, bersih1, bersih2):
    akhir1 = bersih1["Price"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Price"].dropna()
    n = 0
    while n < len(list_regex):
        hasil = re.sub('[DOoU]', '0', str(item))
        hasil = re.sub('[\s]+', '', str(hasil))
        hasil = re.findall(str(list_regex[n]), str(hasil))
        if len(hasil) == 0:
            n = n + 1
            hasil = ''
        else:
            n = len(list_regex)
            hasil = hasil
    akhir1 = bersih2["Price"].dropna()
    p = 0
    while p < len(akhir1):
        hasil = re.sub(str(akhir1[p]), '', str(hasil))
        p = p + 1
    if (len(hasil) == 0) or (len(hasil) < max_char):
        hasil = [item, "NOT CONFIDENT"]
    else:
        hasil = [hasil, "CONFIDENT"]
    return hasil


def clean_unit(item, ambil, bersih1, bersih2):
    akhir1 = bersih1["Unit"].dropna()
    p = 0
    while p < len(akhir1):
        item = re.sub(str(akhir1[p]), '', str(item))
        p = p + 1

    list_regex = ambil["Unit"].dropna()
    n = 0
    while n < len(list_regex):
        hasil2 = re.findall(str(list_regex[n]), str(item))
        if len(hasil2) == 0:
            n = n + 1
            hasil2 = ''
        else:
            n = len(list_regex)
            hasil2 = hasil2
    if len(hasil2) == 0:
        hasil2 = ''
    else:
        hasil2 = hasil2[0]

    akhir1 = bersih2["Unit"].dropna()
    p = 0
    while p < len(akhir1):
        hasil2 = re.sub(str(akhir1[p]), '', str(hasil2))
        p = p + 1

    if len(hasil2) == 0:
        hasil2 = [item, "NOT CONFIDENT"]
    else:
        hasil2 = [hasil2, "CONFIDENT"]
    return hasil2
