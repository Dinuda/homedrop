from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask import g
from bs4 import BeautifulSoup
import requests
from flask import Response
from werkzeug.utils import secure_filename
from flask import send_from_directory



app = Flask(__name__,  static_url_path='',
            static_folder='static', template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'M@hpshinyblack'
app.config['MYSQL_DB'] = 'home_delivery'

mysql = MySQL(app)

# ?category=1&location=2
@app.route('/')
def index():
    locationId = request.args.get("location")
    categoryId = request.args.get("category")

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


@app.route('/vendor/<vendorid>')
def vendor(vendorid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM home_delivery.vendors where id =" + vendorid + ";")
    vendor = cur.fetchall()

    #get phone numbers
    cur.execute("SELECT * FROM home_delivery.contacts where vendor=" + vendorid + ";")
    phones = cur.fetchall()
    print(phones)

    return render_template('vendor_detail.html ', vendor=vendor[0], phones=phones)

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
    vendor = None
    contacts = None

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
    vendor = request.form['vendor']
    url = 'http://www.textit.biz/sendmsg?id=94767819556&pw=6476&to=' + phone + '&text=' + message 
    print(url)
    response = requests.get(url)
    print(response)
    print(phone)
    return redirect('/vendor/' + vendor)

@app.route('/sendmessage' , methods= ['POST'])
def sendmessage():
    phone = request.form['phone']
    return render_template('message.html' , phone=phone)

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
