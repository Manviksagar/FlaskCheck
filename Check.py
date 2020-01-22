from flask import Flask, render_template
from flask import redirect
from flask import url_for, request

app = Flask(__name__)

import sqlite3

app = Flask(__name__)


@app.route("/crud")
def crud():
   return render_template("crud.html");


@app.route("/add")
def add():
   return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
   msg = "msg"
   if request.method == "POST":
      try:
         name = request.form["name"]
         email = request.form["email"]
         address = request.form["address"]
         with sqlite3.connect("employee.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into Employees (name, email, address) values (?,?,?)", (name, email, address))
            con.commit()
            msg = "Employee successfully Added"
      except:
         con.rollback()
         msg = "We can not add the employee to the list"
      finally:
         return render_template("success.html", msg=msg)
         con.close()


@app.route("/view")
def view():
   con = sqlite3.connect("employee.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute("select * from Employees")
   rows = cur.fetchall()
   return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
   return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
   id = request.form["id"]
   with sqlite3.connect("employee.db") as con:
      try:
         cur = con.cursor()
         cur.execute("delete from Employees where id = ?", id)
         msg = "record successfully deleted"
      except:
         msg = "can't be deleted"
      finally:
         return render_template("delete_record.html", msg=msg)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/urls")
def urls():
   return render_template("Urls.html")


@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

@app.route('/stu')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)