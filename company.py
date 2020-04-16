from flask import redirect, render_template
import requests
from werkzeug.utils import secure_filename



def editCompany(mysql, id):
    vendor = None
    contacts = None
    images = None
    locations = None
    vendor_locations = None
    if id:
        print('edit:' + str(id))
        cur = mysql.connection.cursor()
        #get vendor
        cur.execute("select * from vendors where id=%s", [id])
        vendor_result = cur.fetchall()
        vendor = vendor_result[0]
        #get contacts
        cur.execute("SELECT * FROM contacts where vendor=%s" , [id])
        contacts = cur.fetchall()
        print(contacts)
        #get images
        cur.execute("SELECT * FROM images where vendor=%s " , [id])
        images = cur.fetchall()
        print(images)
        #get locations
        cur.execute("SELECT * FROM locations")
        locations = cur.fetchall()
        print(locations)
        #get vendor location where vendor=%s
        cur.execute('''SELECT vendor_locations.*,locations.location as location_name FROM home_delivery.vendor_locations 
                        left outer join home_delivery.locations 
                        on home_delivery.vendor_locations.location =home_delivery.locations.id where vendor=%s''', [id])
        vendor_locations = cur.fetchall()
        print(vendor_locations)
        cur.close()
    else:
        print('create a new company')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories;")
    categories = cur.fetchall()
    cur.close()
    return render_template('edit_company.html',categories=categories, vendor=vendor ,contacts=contacts ,images=images,locations=locations, vendor_locations=vendor_locations)

def editSubmit(mysql, name, site, category, id):
    if id:
        print('update')
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE home_delivery.vendors SET name=%s , site=%s , category=%s  WHERE id=%s",(name ,  site , category, id ))    
        mysql.connection.commit()
        cursor.close()
    else:
        print('insert')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO home_delivery.vendors(name , site , category) VALUES (%s,%s,%s)",(name , site ,category ))    
        mysql.connection.commit()
        id = cursor.lastrowid
        print("inserted:" + str(id))
        cursor.close()

    return redirect('/edit_company?id=' + str(id))

def editFlyer(mysql,id,upload):
    print('image for:' + str(id))
    file_name = str(secure_filename(upload.filename))
    image_path = 'images/'+ file_name
    upload.save(image_path)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO images (vendor, image) VALUES (%s,%s)",(id,file_name))
    mysql.connection.commit()
    cursor.close()
    
    return redirect('/edit_company?id=' + id)

def editDeleteImg(mysql,id,vendor):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM images where id=%s " , [id])
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor)) 

def editContact(mysql,vendor,contact,detail,whatsapp,viber,call,SMS):
    sql = "INSERT INTO home_delivery.contacts(vendor , phone , detail, whatsapp, viber, callnum, messege) VALUES ({0},'{1}','{2}',{3},{4},{5},{6})".format(vendor , contact, detail, whatsapp, viber, call, SMS)
    print(sql)
    cur = mysql.connection.cursor()
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor)) 

def editDeleteContact(mysql, id, vendor):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts where id=%s " , [id])
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor)) 

def editDeleteLocation(mysql, id, vendor_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vendor_locations where id=%s " , [id])
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor_id)) 







