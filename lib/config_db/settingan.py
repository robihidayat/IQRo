import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config/configdb.ini")

def import_config_db():
    IP = Config.get('Database', 'IP')
    User = Config.get('Database', 'User')
    Password =  Config.get('Database', 'Password')
    Database = Config.get('Database', 'Database')
    # strings = str(IP)+"'"+","+"'"+str(User)+"'"+","+"'"+str(Password)+"'"+","+"'"+str(Database)
    return {'IP': IP, 'User':User, 'Password':  Password, 'Database': Database,  }
