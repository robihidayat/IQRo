from lib.config_db.settingan import import_config_db

import MySQLdb as mdb
conf = import_config_db()
settingan = import_config_db()
con = mdb.connect(settingan['IP'],settingan['User'],settingan['Password'],settingan['Database'])



def make_tables_medicine():
    """
    Create Table Medicine
    :return:
    """
    cursor = con.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS Table_Medicine (
           id INT NOT NULL AUTO_INCREMENT,
           PFC INT (11),
           Pack VARCHAR (255),
           Company VARCHAR (255),
           pack_cleanshing TEXT,
           PRIMARY KEY (id),
           FULLTEXT idx (pack_cleanshing)
           ) ENGINE=MyISAM DEFAULT CHARSET=utf8
           '''
    cursor.execute(sql)



def make_table_shop():
    """
    Create Table Shop
    :return:
    """
    cursor = con.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS Table_Shops (
           id INT NOT NULL AUTO_INCREMENT,
           shop VARCHAR (255),
           shop_clean TEXT,
           address VARCHAR (255),
           address_clean TEXT,
           lat_long VARCHAR (255),
           PRIMARY KEY (id),
           FULLTEXT idx (shop_clean),
           FULLTEXT idy (address_clean)
           ) ENGINE=MyISAM DEFAULT CHARSET=utf8
           '''
    cursor.execute(sql)


def make_table_stopwords():
    """
    Create Table stopwords
    :return:
    """
    cursor = con.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS Table_StopWords (
              id INT NOT NULL AUTO_INCREMENT,
              stopwords VARCHAR (255),
              PRIMARY KEY (id)
              ) ENGINE=MyISAM DEFAULT CHARSET=utf8
              '''
    cursor.execute(sql)

if __name__ == '__main__':
    pass

