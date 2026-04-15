from flask import Flask, request
import sqlite3
import os

app =  Flask(__name__)

# Home Page
@app.route('/')
def home():
	return """
	<h2>Vulnerable Web Application</h2>
	<p>Available endpoints</p>
	<ul>
		<li>/login?user=admin&pass=admin123</li>
		<li>/search?q=test</li>
		<li>/file?name=test.txt</li>
	</ul>
	"""

# SQL Injection Vulnerable Login
@app.route('/login')
def login():
	user = request.args.get('user')
	password = request.args.get('pass')

	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()

	query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (user, password)

	result = cursor.execute(query).fetchall()

	if result:
		return "<h3>Login Successful!</h3>"
	else:
		return "<h3>Login Failed!</h3>"

# XSS Vulnerable Search
@app.route('/search')
def search():
	query = request.args.get('q')
	return "<h3>Search results for: " + query + "</h3>"

# Path Traversal Vulnerable FIle Reader
@app.route('/file')
def file():
	filename = request.args.get('name')

	try:
		filepath = os.path.abspath(filename)

		with open(filename, "r") as f:
			data = f.read()
		return "<pre>" + data + "</pre>"
	except:
		return "File not found: " + str(e)

app.run(host='0.0.0.0', port=5000)
