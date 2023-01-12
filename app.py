from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import re

app= Flask(__name__)
             
app.secret_key = 'arvind'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'geri'
mysql = MySQL(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form:
        username = request.form['mail_id']
        password = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE mail_id = % s AND passwd = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['mail_id'] = account['mail_id']
            msg = 'Logged in successfully !'
            return render_template('userindex.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/createlogin', methods =['GET', 'POST'])
def createlogin():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form:
        conn=mysql.connect
        cursor=conn.cursor()
        mail_id = request.form['mail_id']
        passwd = request.form['passwd']
        cursor.execute('SELECT * FROM login WHERE mail_id = % s', (mail_id, ))
        patient = cursor.fetchone()
        if patient:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO login VALUES (% s, % s)', (mail_id, passwd))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    else:
        msg = 'Please fill out the form !'
    return render_template('4_R1_Create_Login.html', msg = msg)

@app.route('/userindex',methods=["GET","POST"])   
def userindex():
    return render_template("userindex.html") 

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template("index.html")  

gds_score=0
@app.route('/gdsuser',methods=['GET','POST'])
def gdsuser():
    global gds_score
    if request.method == "POST":
        gds_score=0
        if len(request.form)==15:
            for i in range(1,16):
                if request.form.get("q"+str(i))=="yes":
                    gds_score+=1
            return redirect(url_for("score"))
    else:
        if "score" in session:
            return redirect(url_for("score"))
    return render_template("7_GDS_Test(User).html")

@app.route("/score",methods=['GET','POST'])
def score():
    if request.method=="POST":
        return render_template("userindex.html")
    return render_template("score.html",title="GDS score",header="Geriatric Depression scale",SCORE=str(gds_score),img="https://cdn.i-scmp.com/sites/default/files/d8/images/canvas/2022/05/10/fed7541e-85cd-4a6d-a4c2-35532cca141e_aba6ccd9.jpg",line1="(>= 10) - You are under deppression",TOTAL_SCORE="15")

mini_score=0
@app.route('/minicoguser',methods=['GET','POST'])
def minicoguser():
    global mini_score
    if request.method=="POST" and len(request.form)==4:
        mini_score=0
        for i in range(1,len(request.form)+1):
            mini_score+=int(request.form.get("q"+str(i)))
        return render_template("score.html",title="MINICOG score",header="MINICOG TEST",SCORE=str(mini_score),img="https://www.associatedneurologists.com/wp-content/uploads/2019/02/WISC-1.png",line1="(< 3) - Possibility of dementia",line2="(>= 3) - May not have dementia (not ruling out entire probability)",TOTAL_SCORE="5")
    return render_template("8_Mini_Cog(User).html") 

mns_score=0
@app.route('/mnsuser',methods=['GET','POST'])
def mnsuser(): 
    global mns_score
    if request.method=="POST" and len(request.form)==6:
        mns_score=0
        for i in range(1,len(request.form)+1):
            mns_score+=int(request.form.get("q"+str(i)))
        return render_template("score.html",title="MNS score",header="My Nutrition Scale",SCORE=str(mns_score),img="https://img.freepik.com/premium-vector/meat-eater-vs-vegetarian-meals-choice_87771-10754.jpg?w=996",line1="12 - 14: Normal nutritional status",line2="8 - 11: At risk of malnutrition",line3="0 - 7: Malnourished",TOTAL_SCORE="14")
    return render_template("9_MNS_Test(User).html")

@app.route('/gdsadmin',methods=['GET','POST'])
def gdsadmin():
    return render_template("7_GDS_Test(Admin).html")

@app.route('/minicogadmin',methods=['GET','POST'])
def minicogadmin():
    return render_template("8_Mini_Cog(Admin).html")

@app.route('/mnsadmin',methods=['GET','POST'])
def mnsadmin():
    return render_template("9_MNS_Test(Admin).html")  
      
@app.route('/registeration',methods=['GET','POST'])
def registeration():
    msg1=''
    if 'loggedin' in session:
        if request.method == 'POST' and 'firstname' in request.form and 'secondname' in request.form and 'dob' in request.form and 'age' in request.form and 'phone' in request.form and 'aphone' in request.form and 'street' in request.form  and 'street1' in request.form and 'street2' in request.form and 'pincode' in request.form and 'state' in request.form:
            conn=mysql.connect
            cursor=conn.cursor()
            mail_id=session['mail_id']
            firstname=request.form['firstname']
            secondname=request.form['secondname']
            dob=request.form['dob']

            age = request.form['age']
            phone = request.form['phone']
            aphone=request.form['aphone']
            street=request.form['street']
            street1=request.form['street1']
            street2=request.form['street2']
            pincode=request.form['pincode']
            state=request.form['state']
            
            if  re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
                msg1 = 'Invalid email address !'
            else:
                cursor.execute('INSERT INTO patient values (%s , % s,  % s,  % s,  % s,  % s,  % s, % s, % s, % s, %s,%s)', (mail_id, firstname, secondname, dob, age, phone, aphone,street,street1,street2,pincode,state))
                conn.commit()
                msg1 = 'You have successfully updated !'
        elif request.method == 'POST':
            msg1 = 'Please fill out the form !'
        return render_template("Registration_2_Personal.html", msg1=msg1)
    return redirect(url_for('userindex'))

@app.route('/profile',methods=['GET','POST'])
def profile():
    return render_template("profile.html")
@app.route('/profilecopy',methods=['GET','POST'])
def profilecopy():
    return render_template("profile copy.html")
@app.route('/medical1',methods=['GET','POST'])
def medical1():
    return render_template('Registration_3_Medical.html')
@app.route('/myrecord',methods=['GET','POST'])
def myrecord():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (session['mail_id'], ))
        login = cursor.fetchone()
        return render_template("myrecord.html", login = login)
    return redirect(url_for('login'))
@app.route('/table',methods=['GET','POST'])
def table():
    if request.method == 'POST' and 'patient' in request.form:
                mail_id=request.form['patient']
                conn=mysql.connect
                cursor=conn.cursor()
                cursor.execute('SELECT * FROM patient WHERE mail_id = % s', (mail_id, ))
                record=cursor.fetchall()
                conn=mysql.connect
                cursor=conn.cursor()
                cursor.execute('SELECT * FROM testscores WHERE mail_id = % s', (mail_id, ))
                display=cursor.fetchall()
                return render_template("tables.html", record=record,display=display)
    return redirect(url_for('index'))   
if __name__=='__main__':
    
	app.run(debug=True)	
