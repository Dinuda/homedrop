
from flask_mysqldb import MySQL

def getDatabase(application):
    application.config['MYSQL_HOST'] = 'shopup.c5qdsuoy5mft.ap-south-1.rds.amazonaws.com'
    application.config['MYSQL_USER'] = 'admin'
    #application.config['MYSQL_PASSWORD'] = 'M@hpshinyblack'
    application.config['MYSQL_PASSWORD'] = 'ShopUpAdmin'
    application.config['MYSQL_DB'] = 'home_delivery'

    return MySQL(application)  