from flask import redirect, render_template


def homepage(mysql, locationId, categoryId):
    cur = mysql.connection.cursor()
    sql = '''SELECT vendors.*  from vendors 
        left join vendor_locations on (vendors.id= vendor_locations.vendor) 
        where 1=1 '''

    if (locationId is not None):
        sql = sql + " and vendor_locations.location=" + locationId

    if (categoryId is not None):
        sql = sql + " and vendors.category=" + categoryId
    
    cur.execute(sql)
    vendors = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home_delivery.locations;")
    locations = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home_delivery.categories;")
    categories = cur.fetchall()

    return render_template('index.html', locations=locations, categories=categories, vendors=vendors)
