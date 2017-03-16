from lib.updatedb.update_db import update_shop, update_medicine
from lib.model.makedictionary import query_dic_string_medicine, query_dic_string_shop, query_dic_string_address
import time

try:
    start = time.time()
    update_shop('database/test_shop_update.csv')
    update_medicine('database/test_medicine_update.csv')
    end = time.time()
    print "Success Update Database took %g s" % (end - start)
except:
    print "error update"

try:
    start = time.time()
    query_dic_string_medicine()
    query_dic_string_shop()
    query_dic_string_address()
    end = time.time()
    print "Success Update Dict took %g s" % (end - start)
except:
    print "error query"