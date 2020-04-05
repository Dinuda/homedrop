from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import g
import requests
from flask import Response
from flask import send_from_directory

import database
import index
import vendor
import company

app = Flask(__name__,  static_url_path='',
            static_folder='static', template_folder='templates')

mysql = database.getDatabase(app)

@app.context_processor
def inject_filter_menu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home_delivery.locations;")
    locations = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home_delivery.categories;")
    categories = cur.fetchall()

    return dict(locations=locations, categories=categories)


# ?category=1&location=2
@app.route('/')
def homePage():
    locationId = request.args.get("location")
    categoryId = request.args.get("category")
    return index.homepage(mysql, locationId, categoryId)


@app.route('/vendor')
def vendorDetail():
    vendorid = request.args.get("id")
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
    return user.userReg(mysql, id)


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
    return company.editSubmit(mysql, name, site, category, id)
   
@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form['message']
    phone = request.form['phone']
    vendorid = request.form['vendor']
    return vendor.vendorSendMessage(message, phone, vendorid)


@app.route('/submit_flyer_edit_company', methods= ['POST'])
def submit_flyer_edit_company():
    id = request.form['id']
    upload = request.files['upload']
    return company.editFlyer(mysql,id, upload)


@app.route('/submit_contacts_edit_company' , methods= ['POST'])
def submit_contacts_edit_company():
    vendor = request.form['id']
    print(vendor)
    contact = request.form['contact']
    return company.editContact(mysql,vendor,contact)

@app.route('/img/<path:filename>')  
def send_file(filename):  
    return send_from_directory('images//', filename)

@app.route('/delete_img' )
def delete_img():
    id = request.args.get("id")
    vendor = request.args.get("vendor")
    return company.editDeleteImg(mysql,id,vendor)

@app.route('/delete_phone')
def delete_phone():
    id = request.args.get("id")
    vendor = request.args.get("vendor")
    return company.editDeleteContact(mysql, id, vendor)