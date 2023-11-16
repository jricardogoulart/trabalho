from flask import Flask, render_template, request,redirect, url_for,flash
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/studentLogin')
def studentLogin():
   return render_template('studentLogin.html')

@app.route('/secretaryLogin')
def secretaryLogin():
   return render_template('secretaryLogin.html')

if __name__ == '__main__':
    app.run(debug=True)