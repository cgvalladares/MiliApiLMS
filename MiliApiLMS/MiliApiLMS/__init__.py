from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

#importar blue print
from MiliApiLMS.routes.index import index_bp
from MiliApiLMS.routes.fingerprint import finger_bp

app = Flask(__name__)
#Cargar configuraciones
CORS(app)
#app.config.from_object('config.ConfigLocal')
app.config.from_object('config.ConfigTestDev')
#app.config.from_object('config.ConfigQa')
#app.config.from_object('config.ConfigAzureGeo')

#ODJ DB
sqlServer=SQLAlchemy(app)

#registrar Blueprint
app.register_blueprint(index_bp)
app.register_blueprint(finger_bp)

#Ejecuta contex si se necesita
with app.app_context():
    import pytest
    Test=False
    if Test:
        try:
            sqlServer.session.execute(text('SELECT 1'))
            print("Conexion exitosa a la base de datos")
        except Exception as e:
            print("Error al conectar a la base de datos:", e)
        pytest.main(['-v','MiliApiLMS/tests/fingerprintTest/test_toolsFingerprint.py'])
        #sqlServer.create_all()

