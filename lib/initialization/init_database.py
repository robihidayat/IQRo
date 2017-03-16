from lib.model.insert import insert_table_shop, insert_table_medicine, insert_table_stopwords
from lib.model.maketable import *
from lib.model.makedictionary import query_dic_string_medicine, query_dic_string_shop, query_dic_string_address, query_dic_stopwords


def main_init():
    try:
        make_tables_medicine()
        make_table_shop()
        make_table_stopwords()
    except:
        print "Error Make Tables"

    try:
        insert_table_shop()
        insert_table_medicine()
        insert_table_stopwords()
    except:
        print "Error Insert Table"

    try:
        query_dic_string_medicine()
        query_dic_string_shop()
        query_dic_string_address()
        query_dic_stopwords()
    except:
        print "error Query"

