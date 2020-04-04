from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import g
import requests
from flask import Response
from werkzeug.utils import secure_filename
from flask import send_from_directory

import database
import index
import vendor
import company

app = Flask(__name__,  static_url_path='',
            static_folder='static', template_folder='templates')

mysql = database.getDatabase(app)

# ?category=1&location=2
@app.route('/')
def homePage():
    locationId = request.args.get("location")
    categoryId = request.args.get("category")
    return index.homepage(mysql, locationId, categoryId)


@app.route('/vendor/<vendorid>')
def vendorDetail(vendorid):
    vendorId = request.args.get("vendorid")
    return vendor.vendorDetail(mysql ,vendorid)

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    return render_template('user_signup.html')

@app.route('/user_reg', methods=['POST'])
def user_reg():
    name = request.form['name']
    email = request.form['email']
    passw = request.form['passw']
    phone = request.form['phone']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO home_delivery.users(name, email, passw, phone) VALUES (%s, %s, %s, %s)", (name, email, passw, phone))
    mysql.connection.commit()
    cursor.close()
    return redirect('/create_company')

@app.route('/edit_company')
def create_company():
    id = request.args.get("id")
    return company.editCompany(mysql, id)



@app.route('/submit_edit_company' , methods=['POST'])
def new_comp():
    name = request.form['name']
    site = request.form['site']
    category = request.form['category']

    id = request.form.get('id')
    
    if id:
        print('update')
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE home_delivery.vendors SET name=%s , site=%s , category=%s  WHERE id=%s",(name ,  site ,category, id ))    
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

   
@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form['message']
    phone = request.form['phone']
    vendorid = request.form['vendor']
    return vendor.vendorSendMessage(message, phone, vendorid)


@app.route('/submit_flyer_edit_company', methods= ['POST'])
def submit_flyer_edit_company():
    id = request.form['id']
    print('image for:' + str(id))
    upload = request.files['upload']
    file_name = str(secure_filename(upload.filename))
    image_path = 'images\\'+ file_name
    upload.save(image_path)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO images (vendor, image) VALUES (%s,%s)",(id,file_name))
    mysql.connection.commit()
    cursor.close()
    
    return redirect('/edit_company?id=' + id)

@app.route('/submit_contacts_edit_company' , methods= ['POST'])
def submit_contacts_edit_company():
    vendor = request.form['id']
    print(vendor)
    contact = request.form['contact']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO home_delivery.contacts(vendor , phone) VALUES(%s,%s)",(vendor , contact))
    mysql.connection.commit()
    cur.close()

    print('done')
    return redirect('/edit_company?id=' + vendor )

@app.route('/profile')
def profile():
    name = request.form['name']
    contact_1= request.form['phone_1']
    contact_2 = request.form['phone_2']
    site = request.form['site']
    category = request.form['category']
    id = request.form.get('id')
    result = cur.fetchall
    return render_template('profile.html')

@app.route('/img/<path:filename>')  
def send_file(filename):  
    return send_from_directory('images//', filename)

@app.route('/delete_img' )
def delete_img():
    id = request.args.get("id")
    vendor = request.args.get("vendor")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM images where id=%s " , [id])
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor)) 

@app.route('/delete_phone')
def delete_phone():
    id = request.args.get("id")
    vendor = request.args.get("vendor")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts where id=%s " , [id])
    mysql.connection.commit()
    cur.close()

    return redirect('/edit_company?id=' + str(vendor)) 
