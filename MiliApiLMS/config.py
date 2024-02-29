import urllib

class JWT:
    #JWT
    JWT_SECRET_KEY  = 'fgjtd8973aac402d8761016e83767ba4'
    #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiTGVjIn0.AOY8uoWhwCQkzugKoIoXrVDYuU5AYluaVWghUPzovzc
    
class Humbral:
    #humbral hash
    HUMBRAL_DHASH=7

class ConfigLocal:
    DEBUG=True
    TESTING=True
    DRIVER='mssql+pyodbc'
    OTHER='driver=ODBC+Driver 17 for SQL+Server'
    #DB
    DB_SERVER = 'Progra2024-02\SQLSERVERLOCALM'
    DB_USER = 'sa'
    DB_PASSWORD = 'Geo4160150087.'
    DB_NAME = 'Fingerprintt'
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?{OTHER}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=False
    
class ConfigTestDev:
    DEBUG= False
    TESTING= False
    DRIVER='mssql+pymssql'
    #DB
    DB_SERVER = 'sdevtestlec.database.windows.net:1433'
    DB_USER = 'desarrollo'
    DB_PASSWORD = 'C0ntr0lT0t@l'
    DB_NAME = 'CT_Pruebas-2023_11_15-03_00_00'
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_SERVER}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=False
    
class ConfigQa:
    DEBUG= True
    TESTING= False
    DRIVER='mssql+pymssql'
    #DB
    DB_SERVER = 'pruebas-ct.database.windows.net:1433'
    DB_USER = 'desarrollo'
    DB_PASSWORD = 'C0ntr0lT0t@l'
    DB_NAME = 'CT_Pruebas-2024_02_09-03_00_00'
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_SERVER}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=False
    
class ConfigAzureGeo:
    DEBUG= True
    TESTING= False
    DRIVER='mssql+pymssql'
    #DB
    DB_SERVER = 'virtualpiserver.database.windows.net:1433'
    DB_USER = 'geo22'
    DB_PASSWORD = 'Geo4160150087.'
    DB_NAME = 'apirestlmsdb'
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_SERVER}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True
    