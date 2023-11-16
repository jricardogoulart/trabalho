from flask import Flask, render_template, request,redirect, url_for,flash
import mysql.connector

# db = mysql.connector.connect
# (host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
#  user='aluno_fatec', password='aluno_fatec',database='meu_banco')

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