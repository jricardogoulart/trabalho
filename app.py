from flask import Flask, render_template, request,redirect, url_for,flash
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
        host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user='aluno_fatec',
        password='aluno_fatec',
        database='meu_banco'
    )

mycursor = db.cursor()

# Rota da página inicial
@app.route('/')
def index():
 return render_template('index.html')

# Rotas de Exibição das telas de login
@app.route('/studentLoginScreen')
def studentLoginScreen():
   return render_template('studentLoginScreen.html')

@app.route('/secretaryLoginScreen')
def secretaryLoginScreen():
   return render_template('secretaryLoginScreen.html')

# Rotas para logar
@app.route('/secretaryLogin', methods=['POST'])
def secretaryLogin():

    login = request.form.get('login')
    senha = request.form.get('senha')

    select_query = 'SELECT * FROM ze_TB_academic WHERE login = %s AND senha = %s'
    mycursor.execute(select_query,(login,senha))
    result = mycursor.fetchone()
    
    if result is None:
         # O login falhou, redirecione para a página de login ou exiba uma mensagem de erro
        return 'Usuário Inválido <br> <a href="secretaryLoginScreen">Acesse novamente o Login</a>'      
    else:
         # O login foi bem-sucedido, redirecione para a página principal ou faça o que for necessário
        return secretaryHomeScreen()

   
@app.route('/studentLogin', methods=['POST'])
def studentLogin():
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    select_query = 'SELECT * FROM ze_TB_alunos WHERE cpf = %s AND senha = %s'
    mycursor.execute(select_query,(cpf,senha))
    result = mycursor.fetchone()
    
    if result is None:
         # O login falhou, redirecione para a página de login ou exiba uma mensagem de erro
        return 'Usuário Inválido <br> <a href="studentLoginScreen">Acesse novamente o Login</a>'      
    else:
         # O login foi bem-sucedido, redirecione para a página principal ou faça o que for necessário
        return studentHomeScreen()



# Rotas pós-login
@app.route('/studentHomeScreen')
def studentHomeScreen():
   return render_template ('studentHome.html')

@app.route('/secretaryHomeScreen')
def secretaryHomeScreen():
   return render_template('secretaryHome.html')

# Rotas pós-login das 4 Funções da Secretaria: 
@app.route('/cadastrar_alunos')
def cadastrar_alunos():
    return render_template('cadastrar_alunos.html')

@app.route('/cadastrar_funcionarios')
def cadastrar_funcionarios():
    
    return render_template('cadastrar_funcionarios.html')

@app.route('/cadastrar_disciplinas')
def cadastrar_disciplinas():
    
    return render_template('cadastrar_disciplinas.html')

@app.route('/cadastrar_notas')
def cadastrar_notas():
    
    return render_template('cadastrar_notas.html')

if __name__ == '__main__':
    app.run(debug=True)