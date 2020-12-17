from flask import Flask, request , render_template
import os

import pymysql
import pymysql.cursors


app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


with connection.cursor() as cursor:
    # Create a new record
    sql = "INSERT INTO `Account` (`email`, `password` , `name`) VALUES (%s, %s , %s)"
    cursor.execute(sql, ('wacky@gmail.com', 'QQQQQQ' , 'HaHaOWO'))

connection.commit()


@app.route('/')
def hello():
    if request.method =='POST':
        if request.values['send']=='Search':
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `email`,`name`FROM `Account` WHERE `email`=%s"
                cursor.execute(sql, (request.values['user']))
                result = cursor.fetchone()
                print(result)
                return render_template('index.html',name=result["name"] , id = result["id"])
    return render_template("index.html",name="")

if __name__ == '__main__':
    app.debug = True
    app.run() #啟動伺服器