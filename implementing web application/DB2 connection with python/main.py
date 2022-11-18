from flask import *
from flask_cors import CORS
import ibm_db
import re

app = Flask(__name__)

CORS(app)
cors =CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID=kjf40222;PWD=mbSqNCJVKq3Ecbgi",'','')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/login',methods = ['POST'])
def login():
      uname=request.form['username']
      passwrd=request.form['password']
      sql = "SELECT * FROM users WHERE USERNAME =? AND PASSWORD=?"
      try:
          stmt = ibm_db.prepare(conn, sql)
          ibm_db.bind_param(stmt,1,uname)
          ibm_db.bind_param(stmt,2,passwrd)
          ibm_db.execute(stmt)
          account = ibm_db.fetch_assoc(stmt)
          print (account)
          if account["USERNAME"] == uname and account["PASSWORD"] == passwrd:
              
            
              msg = 'Logged in successfully !'
              print(msg)
              return redirect(url_for("user"))
          else:
            msg = 'Incorrect username / password !'
            print(msg)
            return render_template('index.html')
      except:
            print("Error")
            return redirect(url_for("success"))
      else:
            print("complete")          
      
     


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg =" "
    if request.method == 'POST' :
        username = request.form['username']
        
        password = request.form['password']
        try:
            sql = "SELECT * FROM users WHERE username =?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                  msg = 'Account already exists !'
                  print(msg)
                  return redirect(url_for("reg"))

            else:
                  print("running")
                  print(username)
                  insert_sql = "INSERT INTO  users VALUES (?, ?)"
                  prep_stmt = ibm_db.prepare(conn,insert_sql)
                  ibm_db.bind_param(prep_stmt, 1, username)
                  ibm_db.bind_param(prep_stmt, 2, password)
                  ibm_db.execute(prep_stmt)
                  msg = 'You have successfully registered !'
                  print(msg)
                  return redirect(url_for("user"))
        except:
                  print("error")
                  return redirect(url_for("reg"))

      
    return render_template('register.html')

@app.route('/reg')
def reg(): 
    return render_template('register.html')

@app.route('/about')
def about():
      return render_template('About.html')

@app.route('/Admin')
def admin():
      return render_template('Admin.html')

@app.route('/cart')
def cart():
      return render_template('Cart.html')

@app.route('/contact')
def contact():
      return render_template('Contact.html')


@app.route('/detail')
def detail():
      return render_template('Detail.html')

@app.route('/items')
def items():
      return render_template('Items.html')

@app.route('/success')
def success():
      return render_template('Success.html')

@app.route('/user')
def user():
      return render_template('User.html')

if __name__ == "__main__":
    app.run()

