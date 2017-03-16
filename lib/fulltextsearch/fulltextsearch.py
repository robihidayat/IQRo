'modul untuk full text seaching'
'function terdiri dari function just number, row item, '


from lib.config_db.settingan import import_config_db

import MySQLdb as mdb
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])



def fts_row_obat(inputstring):
    if not inputstring:
        return 'NOT FOUND'
    data = []
    sql = 'SELECT *, MATCH (pack_cleanshing) against ('+"'"+'+'+inputstring+"'"+' in boolean mode) AS score FROM Table_Medicine WHERE MATCH (pack_cleanshing) against ('+"'"+'+'+inputstring+"'"+' in boolean mode) ORDER BY SCORE DESC'
    try:
        with con:
            cur = con.cursor()
            cur.execute(sql)
            cek_split = [row[2] for row in cur]
            if not cek_split:
                return 'NOT FOUND'
            else:
                data = cek_split[0]
                return data

    except:
        return 'NOT FOUND'


def fts_row_code(inputstring):
    if not inputstring:
        return 'NOT FOUND'
    data = []
    sql = 'SELECT *, MATCH (pack_cleanshing) against ('+"'"+'+'+inputstring+"'"+' in boolean mode) AS score FROM Table_Medicine WHERE MATCH (pack_cleanshing) against ('+"'"+'+'+inputstring+"'"+' in boolean mode) ORDER BY SCORE DESC'
    try:
          with con:
            cur = con.cursor()
            cur.execute(sql)
            cek = [row[1] for row in cur]
            if not cek:
                return 'CODE NOT FOUND'
            else:
                return int(cek[0])

    except:
        return 'NOT FOUND'


def confidance_lev(input_string):
    if input_string == None:
        pass
    data = []
    sql = 'select *, count(score) from (select *,match (pack_cleanshing) against ('+"'"+'+'+input_string+"'"+' in boolean mode) as score from table_pack_description_new where match (pack_cleanshing) against ('+"'"+'+'+input_string+"'"+' in boolean mode) order by score desc) a group by score order by score desc'
    try:
          with con:
            cur = con.cursor()
            cur.execute(sql)
            cek = [row[5] for row in cur]
            if not cek:
                return 'CODE NOT FOUND'
            else:
                return int(cek[0])

    except:
        return 'NOT FOUND'


def fts_row_toko(inputstring):
    if inputstring == None:
        inputstring = 'NOT FOUND'
    data = []
    sql = 'SELECT *, MATCH (shop_clean) against ("'+inputstring+'") AS score FROM Table_Shops WHERE MATCH (shop_clean) against ("'+inputstring+'") ORDER BY SCORE DESC'

    try:
        with con:
            cur = con.cursor()
            cur.execute(sql)
            result_set = cur.fetchall()
            cek_split = [row[1] for row in result_set]
            if not cek_split:
                return 'NOT FOUND'
            else:
                data = cek_split[0]
                return data
    except:
        return ''


def fts_row_jalan(inputstring):
    if inputstring == None:
        inputstring = 'NOT FOUND'
    data = []
    sql = 'SELECT *, MATCH (address_clean) against ("'+inputstring+'") AS score FROM Table_Shops WHERE MATCH (address_clean) against ("'+inputstring+'") ORDER BY SCORE DESC'
    try:
        with con:
            cur = con.cursor()
            cur.execute(sql)
            result_set = cur.fetchall()
            cek_split = [row[3] for row in result_set]
            if not cek_split:
                return 'NOT FOUND'
            else:
                data = cek_split[0]
                return data
    except:
        return ''
