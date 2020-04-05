from flask import redirect, render_template


def homepage(mysql, locationId, categoryId):
    cur = mysql.connection.cursor()
    sql = '''select vendors.id, vendors.name, vendors.site, categories.name, first_image.image from vendors 
            left join (select * from images where id in (select min(id) from images group by vendor)) as first_image on vendors.id = first_image.vendor
            join categories on (vendors.category = categories.id)'''

    if locationId:
        sql = sql + " left join vendor_locations on (vendors.id = vendor_locations.vendor and vendor_locations.location = " + locationId + ")"

    if categoryId:
        sql = sql + " where categories.id = " + categoryId + ""
    
    cur.execute(sql)
    vendors = cur.fetchall()

    return render_template('index.html', vendors=vendors)
