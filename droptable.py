import MySQLdb as mdb
con = mdb.connect('127.0.0.1', 'root', '', 'test')


def iter_table():
    datas = []
    cursor = con.cursor()
    sql = "show tables"
    cursor.execute(sql)
    tables = cursor.fetchall()
    for row in tables:
        datas.append(row[0])
    return datas


def empty_table():
    cursor = con.cursor()
    datas = iter_table()
    for row in datas:
        sql = "truncate table "+row
        cursor.execute(sql)
    print "sukses empty"

if __name__ == '__main__':
    empty_table()