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
#Cadastrar Aluno e Salvar Cadastro:
@app.route('/cadastrar_alunos',methods=['GET','POST'])
def cadastrar_alunos():
    if request.method =='GET':
     
     select_query = "SELECT id, nome, cpf FROM ze_TB_alunos"
     mycursor.execute(select_query)
     resultado = mycursor.fetchall()

     return render_template('cadastrar_alunos.html',alunos = resultado)
    
    if request.method == 'POST':
        
     nome = request.form.get('nome')
     cpf = request.form.get('cpf')
     senha = request.form.get('senha')

     select_query = 'INSERT INTO  ze_TB_alunos (cpf,nome,senha) VALUES(%s,%s,%s)'
     mycursor.execute(select_query,(cpf,nome,senha))
     db.commit()

     return redirect(url_for('cadastrar_alunos'))
    
    return render_template('cadastrar_notas.html')

#Atualizar aluno cadastrado
@app.route('/updateAluno')
def updateAluno():
    return render_template('atualizar_alunos.html')

#Cadastrar Funcionário e Salvar Cadastro:
@app.route('/cadastrar_funcionarios',methods=['GET','POST'])
def cadastrar_funcionarios():
    if request.method == "GET":
     
     select_query = "SELECT id, cpf, nome, email, login from ze_TB_academic"
     mycursor.execute(select_query)
     resultado = mycursor.fetchall()

     return render_template('cadastrar_funcionarios.html',academic = resultado)

    if request.method == "POST":
     
     nome = request.form.get('nome')
     email = request.form.get('email')
     cpf = request.form.get('cpf')
     login = request.form.get('login')
     senha = request.form.get('senha')
    
     select_query = 'INSERT INTO  ze_TB_academic (nome,email,cpf,login,senha) VALUES(%s,%s,%s,%s,%s)'
     mycursor.execute(select_query,(nome,email,cpf,login,senha))
     db.commit()
    
     return redirect(url_for('cadastrar_funcionarios'))
    
    return render_template('cadastrar_funcionarios.html')

#Atualizar Cadastro do funcionário
@app.route('/updateAcademic')
def updateAcademic():

    return render_template('atualizar_funcionarios.html')

#Cadastrar Disciplina e Salvar Cadastro:   
@app.route('/cadastrar_disciplinas', methods=['GET','POST'])
def cadastrar_disciplinas():

    if request.method == 'GET':
     
     select_query = 'SELECT * FROM ze_TB_disciplina'
     mycursor.execute(select_query)
     disciplina = mycursor.fetchall()
     return render_template('cadastrar_disciplinas.html', disciplinas = disciplina)

    if request.method == 'POST':
     
     disciplina = request.form.get('disciplina')
     select_query = 'INSERT INTO ze_TB_disciplina (disciplina) VALUE(%s)'
     mycursor.execute(select_query,(disciplina,))
     db.commit()

     return redirect(url_for('cadastrar_disciplinas'))
    
    return render_template('cadastrar_funcionarios.html')

#Cadastrar Notas e Salvar Cadastro:
@app.route('/cadastrar_notas', methods=['GET','POST'])
def cadastrar_notas():

    if request.method == 'GET':
        select_query = 'SELECT * FROM ze_TB_alunos '
        mycursor.execute(select_query)
        aluno = mycursor.fetchall()

        select_query1= 'SELECT * FROM ze_TB_disciplina'
        mycursor.execute(select_query1)
        materia = mycursor.fetchall()

        return render_template('cadastrar_notas.html', alunos = aluno, materias = materia)
    
    if request.method == 'POST':

        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])
        nota4 = float(request.form['nota4'])
        media = round((nota1 + nota2 + nota3 + nota4)/4,2)
        idAluno = request.form.get('selectAluno')
        idMateria = request.form.get('selectMateria')

        select_query = 'INSERT INTO ze_TB_notas (nota1,nota2,nota3,nota4,id_Aluno,id_Materia,media) VALUES (%s,%s,%s,%s,%s,%s,%s)'

        mycursor.execute(select_query,(nota1,nota2,nota3,nota4,idAluno,idMateria,media))
        db.commit()
        return redirect(url_for('cadastrar_notas'))
    
    return render_template('cadastrar_notas.html')

if __name__ == '__main__':
    app.run(debug=True)