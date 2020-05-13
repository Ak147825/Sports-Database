from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import re
import time
app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

app.config['MYSQL_HOST'] = 'hostip address'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app1'
mysql = MySQL(app)


@app.route("/signup", methods =["GET","POST"])
def signup():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		value=request.form['subscribe']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address!'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers!'
		elif not username or not password or not email:
			msg = 'Please fill out the form!'
		else:
			cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (email, password,value, username,))
			mysql.connection.commit()
			msg = 'You have successfully registered!'
	elif request.method == 'POST':
		msg = 'Please fill out the form!'
	return render_template('signup.html', msg=msg)
@app.route("/",  methods =["GET","POST"])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = username
			return redirect("/home")
		else:
			msg = 'Incorrect username/password!'
			return redirect("/signup")
	return render_template('login.html', msg=msg)    


			


	#return redirect("/home")	
@app.route('/home',methods = ['GET','POST'])
def index(): 	
	if request.method == 'POST' and 'loggedin' in session:
		userDetails = request.form
		query = userDetails['Query']
		cur = mysql.connection.cursor()
		cur.execute(query)
		mysql.connection.commit()
		alldata = cur.fetchall()
		cur.close()
		return render_template('display.html',userDetails = alldata)
		# return 'query'
	return render_template('f_index.html', username=session['username'])
	# return render_template('index.html')
@app.route("/Showcricketteam/", methods=['POST'])
def Showcricketteam():
    #Moving forward code
	cur = mysql.connection.cursor()
	cur.execute("select * from cricket")
	mysql.connection.commit()
	alldata = cur.fetchall()
	cur.close()
	return render_template('display.html', userDetails=alldata);

@app.route("/Showcteam/", methods=['POST'])
def Showcteam():
    #Moving forward code
	cur = mysql.connection.cursor()
	cur.execute("select * from teams")
	mysql.connection.commit()
	alldata = cur.fetchall()
	cur.close()
	return render_template('display.html', userDetails=alldata);
    # forward_message = "Moving Forward..."

# @app.route('/showplayers')
# def showplayers():
# 	cur = mysql.connection.cursor()
# 	cur.execute("Select * from cricket")
# 	mysql.connection.commit()
# 	alldata = cur.fetchall()
# 	cur.close()
# 	return render_template('display.html',userDetails = alldata)
def checkf():
	print("hello hellooo")


if __name__ == '__main__':
	app.run(debug = True)
