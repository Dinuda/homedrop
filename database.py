
from flask_mysqldb import MySQL

def getDatabase(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'M@hpshinyblack'
    #app.config['MYSQL_PASSWORD'] = 'mysqlroot'
    app.config['MYSQL_DB'] = 'home_delivery'

    return MySQL(app)  