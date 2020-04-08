from flask import redirect, render_template


def homepage(mysql, locationId, categoryId):
    cur = mysql.connection.cursor()
    sql = '''select vendors.id, vendors.name, vendors.site, categories.name, first_image.image from vendors 
            left join (select * from images where id in (select min(id) from images group by vendor)) as first_image 
            on vendors.id = first_image.vendor
            join categories on (vendors.category = categories.id)
            {location_join} where 1=1 {location_where} {category_where}'''

    location_join = ""
    location_where = ""
    category_where = ""
    if locationId:
        location_join = " left join vendor_locations on (vendors.id = vendor_locations.vendor)"
        location_where = " and vendor_locations.location = " + locationId 

    if categoryId:
        category_where = " and categories.id = " + categoryId + ""
    
    sql = sql.format(location_join=location_join, location_where=location_where, category_where=category_where)
    print(sql)
    cur.execute(sql)
    vendors = cur.fetchall()

    return render_template('index.html', vendors=vendors)
