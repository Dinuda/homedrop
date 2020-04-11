from flask import redirect, render_template
import requests


def vendorDetail(mysql , vendorid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT vendors.id, vendors.name, vendors.site ,categories.name FROM home_delivery.vendors left outer join home_delivery.categories on (vendors.category =categories.id ) where vendors.id =" + vendorid + ";")
    vendor = cur.fetchall()

    #get phone numbers
    cur.execute("SELECT * FROM home_delivery.contacts where vendor=" + vendorid + ";")
    phones = cur.fetchall()
    print(phones)

    #get images for vendor
    cur.execute("SELECT * FROM home_delivery.images where vendor=" + vendorid + ";")
    images = cur.fetchall()
    print(images)

    return render_template('vendor.html' , vendor=vendor[0],  phones=phones, images = images  )


def vendorSendMessage(message, phone, vendorid):
    url = 'http://www.textit.biz/sendmsg?id=94767819556&pw=6476&to=' + phone + '&text=' + message 
    print(url)
    response = requests.get(url)
    print(response)
    print(phone)
    message = "text message sent to vendor"
    return redirect('/vendor?id=' + vendorid + '&message=' + message)

