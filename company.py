from flask import redirect, render_template
import requests

def editCompany(mysql, id):
    vendor = None
    contacts = None
    images = None
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
        cur.close()
    else:
        print('create a new company')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories;")
    categories = cur.fetchall()
    cur.close()
    return render_template('edit_company.html',categories=categories, vendor=vendor ,contacts=contacts ,images=images)
