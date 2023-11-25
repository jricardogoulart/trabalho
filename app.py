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

#Cadastrar Aluno:
@app.route('/cadastrar_alunos')
def cadastrar_alunos():

    select_query = "select id, nome from ze_TB_alunos"
    mycursor.execute(select_query)
    resultado = mycursor.fetchall()

    return render_template('cadastrar_alunos.html',alunos = resultado)

@app.route('/saveStudent',methods=['POST'])
def saveStudent():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    senha = request.form.get('senha')

    select_query = 'INSERT INTO  ze_TB_alunos (cpf,nome,senha) VALUES(%s,%s,%s)'
    mycursor.execute(select_query,(cpf,nome,senha))
    db.commit()

    return redirect(url_for('cadastrar_alunos'))

@app.route('/cadastrar_funcionarios')
def cadastrar_funcionarios():
    return render_template('cadastrar_funcionarios.html')

@app.route('/saveAcademic', methods=['POST'])
def saveAcademic():
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    login = request.form.get('login')
    senha = request.form.get('senha')
    
    select_query = 'INSERT INTO  ze_TB_academic (nome,email,cpf,login,senha) VALUES(%s,%s,%s,%s,%s)'
    mycursor.execute(select_query,(nome,email,cpf,login,senha))
    db.commit()
    
    return 'Funcionário Cadastradado com Sucesso! <br> <a href="secretaryHomeScreen">Acesse novamente a Home</a>'
    
@app.route('/cadastrar_disciplinas')
def cadastrar_disciplinas():
    return render_template('cadastrar_disciplinas.html')

@app.route('/saveDisciplina',methods=['POST'])
def saveDisciplina():
    
    disciplina = request.form.get('disciplina')

    select_query = 'INSERT INTO ze_TB_disciplina (disciplina) VALUE(%s)'
    mycursor.execute(select_query,(disciplina,))
    db.commit()

    return 'Disciplina Cadastrada com Sucesso! <br> <a href="secretaryHomeScreen"> Acesse novamente a Home</a>'

@app.route('/cadastrar_notas')
def cadastrar_notas():
    return render_template('cadastrar_notas.html')

if __name__ == '__main__':
    app.run(debug=True)