"""
http://stackoverflow.com/questions/3164505/mysql-insert-record-if-not-exists-in-table
"""

import MySQLdb as mdb
from lib.fulltextsearch.dictionary_fts import make_kamus_medicine
from lib.fulltextsearch.dictionary_shop import make_kamus_shop
from prygress import progress
from lib.config_db.settingan import import_config_db
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])

cursor = con.cursor()


def main_update_medicine(df):
    for index, row in df.iterrows():
        sql = "INSERT INTO Table_Medicine (PFC, Pack, Company, pack_cleanshing) SELECT * FROM (SELECT "+"'"+str(row['PFC']).replace("'"," ")+ "'"+","+ "'"+row['Pack'].replace("'"," ")+"'"+" as Pack"+","+ "'"+row['Company'].replace("'"," ")+"'"+"as Company"+" ,"+"'"+row['pack_cleanshing'].replace("'"," ")+"'"+"as pack_cleanshing"+") AS tmp WHERE NOT EXISTS (SELECT Pack FROM Table_Medicine WHERE Pack = "+ "'"+row['Pack'].replace("'"," ")+"'"+") LIMIT 1"
        cursor.execute(sql)
        con.commit()


def main_update_shops(df):
    for index, row in df.iterrows():
        sql = "INSERT INTO Table_Shops (shop, shop_clean, address, address_clean, lat_long) SELECT * FROM (SELECT "+"'"+str(row['shop']).replace("'"," ")+ "'"+ "as shop" +","+ "'"+str(row['shop_clean']).replace("'"," ")+"'"+" as shop_clean"+","+ "'"+row['address'].replace("'"," ")+"'"+" as address"+","+ "'"+row['address_clean'].replace("'"," ")+"'"+" as address_clean"+" ,"+"'"+str(row['lat_long'])+"'"+ ") AS tmp WHERE NOT EXISTS (SELECT shop FROM Table_Shops WHERE shop = "+ "'"+row['shop'].replace("'"," ")+"'"+") LIMIT 1"
        cursor.execute(sql)
        con.commit()


@progress
def update_medicine(files):
    medicine = make_kamus_medicine(files)
    main_update_medicine(medicine)


@progress
def update_shop(files):
    shops = make_kamus_shop(files)
    main_update_shops(shops)



