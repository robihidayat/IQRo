# # from lib.initialization.init_database import main_init
# # from lib.cleanshinghmm.cleansing_entity import cleansing_prodDesc
# # from lib.cleanshingregex.cleansing_regex import clean_unit
# # from lib.fulltextsearch.fulltextsearch import fts_row_obat
# # from lib.stringmatching.string_match import ready_to_split
# # from lib.treesearch.tree_search import query_string
# # from lib.treesearch.tree_search_apotek import query_apotek
# # from lib.treesearch.tree_search_jalan import query_jalan
# # from lib.fulltextsearch.fulltextsearch import fts_row_toko
# # print fts_row_toko('new')
# # print query_jalan('JL KESEHATAN 100')
# # main_init()
# # print cleansing_prodDesc('Panadol COld dan FLu')
# # print clean_unit('12 BTL')
# # print fts_row_obat('cortison')
# # print ready_to_split('Split10 20MG')
# # print query_string('Cortison')
# # print query_apotek('CORTISON Kimia Farma')
# # from lib.parse.parse_html import ParseTable
# # main_init()
# # from lib.updatedb.update_db import update_shop
# # update_shop('database/test_shop_update.csv')
#
#
# from lib.config_db.settingan import import_config_db
#
# import MySQLdb as mdb
# conf = import_config_db()
# settingan = import_config_db()
# con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])
#
#
