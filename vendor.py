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

    return render_template('vendor.html', vendor=vendor[0], phones=phones)

def vendorSendMessage(message, phone, vendor):
    url = 'http://www.textit.biz/sendmsg?id=94767819556&pw=6476&to=' + phone + '&text=' + message 
    print(url)
    response = requests.get(url)
    print(response)
    print(phone)
    return redirect('/vendor/' + vendor)
