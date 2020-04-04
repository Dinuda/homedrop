def userReg(mysql, id):
    cursor.execute("INSERT INTO home_delivery.users(name, email, passw, phone) VALUES (%s, %s, %s, %s)", (name, email, passw, phone))
    mysql.connection.commit()
    cursor.close()
    return redirect('/create_company')