from lib.config_db.settingan import import_config_db
import MySQLdb as mdb
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])
cursor = con.cursor()


def query_dic_string_medicine():
    sql = "SELECT pack_cleanshing FROM Table_Medicine"
    cursor.execute(sql)
    result = cursor.fetchall()
    with open("dictionary/dictionary_string_match_medicine.txt", "w") as text_file:
        for row in result:
            text_file.write(row[0]+' ')


def query_dic_string_shop():
    sql = "SELECT shop_clean FROM Table_Shops"
    cursor.execute(sql)
    result = cursor.fetchall()
    with open("dictionary/dictionary_string_match_shop.txt", "w") as text_file:
        for row in result:
            text_file.write(row[0]+' ')


def query_dic_string_address():
    sql = "SELECT address_clean FROM Table_Shops"
    cursor.execute(sql)
    result = cursor.fetchall()
    with open("dictionary/dictionary_string_match_address.txt", "w") as text_file:
        for row in result:
            text_file.write(row[0]+' ')


def query_dic_stopwords():
    sql = "SELECT stopwords FROM Table_StopWords"
    cursor.execute(sql)
    result = cursor.fetchall()
    with open("dictionary/dictionary_stopwords.txt", "w") as text_file:
        for row in result:
            text_file.write(row[0]+' ')