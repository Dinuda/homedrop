
from flask_mysqldb import MySQL

def getDatabase(app):
    app.config['MYSQL_HOST'] = 'shopup.c5qdsuoy5mft.ap-south-1.rds.amazonaws.com'
    app.config['MYSQL_USER'] = 'admin'
    #app.config['MYSQL_PASSWORD'] = 'M@hpshinyblack'
    app.config['MYSQL_PASSWORD'] = 'ShopUpAdmin'
    app.config['MYSQL_DB'] = 'home_delivery'

    return MySQL(app)  