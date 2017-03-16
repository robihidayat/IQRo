import MySQLdb as mdb
from lib.fulltextsearch.dictionary_fts import make_kamus_medicine
from lib.fulltextsearch.dictionary_shop import make_kamus_shop
from lib.fulltextsearch.dictionary_stopwords import make_kamus_stopwords
from prygress import progress
from lib.config_db.settingan import import_config_db

import MySQLdb as mdb
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])
cursor = con.cursor()


def main_medicine(df):
    for index, row in df.iterrows():
        medicine = (row['PFC'], str(row['Pack']), str(row['Company']), str(row['pack_cleanshing']))
        sql = "INSERT INTO Table_Medicine(PFC,Pack, Company, pack_cleanshing) VALUES( %s, %s,%s, %s )"
        cursor.executemany(sql, (medicine,))
        con.commit()


def main_shop(df):
    for index, row in df.iterrows():
        shop = (row['shop'], str(row['shop_clean']), str(row['address']), str(row['address_clean']), str(row['lat_long']))
        sql = "INSERT INTO Table_Shops(shop, shop_clean, address, address_clean, lat_long) VALUES( %s, %s, %s, %s, %s)"
        cursor.executemany(sql, (shop,))
        con.commit()


def main_stopwords(df):
    for index, row in df.iterrows():
        sql = "INSERT INTO Table_StopWords (stopwords) VALUES "+"("+"'"+row['stopwords']+"'"+")"+""

        cursor.execute(sql)
        con.commit()


@progress
def insert_table_medicine():
    input_file = make_kamus_medicine(r"database/test_medicine.csv")
    main_medicine(input_file)


@progress
def insert_table_shop():
    input_file = make_kamus_shop(r"database/test_shop.csv")
    main_shop(input_file)


@progress
def insert_table_stopwords():
    input_file = make_kamus_stopwords(r"database/test_stopwords.csv")
    main_stopwords(input_file)