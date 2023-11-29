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
       return render_template('studentLoginScreen.html')
    
    select_query = ('SELECT m.disciplina, n.nota1, n.nota2, n.nota3, n.nota4, n.media FROM ze_TB_notas n INNER JOIN ze_TB_disciplina m ON n.id_Materia = m.id WHERE n.id_Aluno = %s')
    mycursor.execute(select_query,(result[0],))
    materia = mycursor.fetchall()

    return render_template('studentHome.html', result= result, materias = materia)
    

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

#Excluir Aluno
@app.route('/deleteAluno/<aluno>')
def deleteAluno(aluno):
   select_query = "DELETE from ze_TB_alunos where id = '" + aluno + "'"
   print(select_query)
   mycursor.execute(select_query)
   db.commit()
   return redirect(url_for('cadastrar_alunos'))
   

#Atualizar aluno cadastrado
@app.route('/updateAluno/<int:id>', methods=['GET'])
def updateAluno(id):

    select_query = "SELECT * FROM ze_TB_alunos WHERE id = %s"
    mycursor.execute(select_query, (id,))
    aluno = mycursor.fetchone()

    return render_template('atualizar_alunos.html', aluno = aluno)

@app.route('/updateAluno', methods=['POST'])
def update_aluno():
    if request.method == 'POST':

        id = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        senha = request.form['senha']

        select_query = "UPDATE ze_TB_alunos SET nome = %s,cpf = %s,senha = %s WHERE id = %s"
        mycursor.execute(select_query, (nome,cpf,senha,id,))
        db.commit()
        
        return redirect(url_for('cadastrar_alunos'))
    
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

#Excluir Funcionário
@app.route('/deleteFuncionario/<academic>')
def deleteFuncionario(academic):
   select_query = "DELETE from ze_TB_academic where id = '" + academic + "'"
   print(select_query)
   mycursor.execute(select_query)
   db.commit()
   return redirect(url_for('cadastrar_funcionarios'))

#Atualizar Cadastro do funcionário
@app.route('/updateAcademic/<int:id>', methods=['GET'])
def updateAcademic(id):

    select_query = "SELECT * FROM ze_TB_academic WHERE id = %s"
    mycursor.execute(select_query, (id,))
    academic = mycursor.fetchone()

    return render_template('atualizar_funcionarios.html', academic = academic)

@app.route('/updateAcademic', methods=['POST'])
def update_academic():

    if request.method == 'POST':

        id = request.form['id']
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        login = request.form['login']
        senha = request.form['senha']

        select_query = "UPDATE ze_TB_academic SET cpf = %s,nome = %s,email = %s, login = %s, senha = %s WHERE id = %s"
        mycursor.execute(select_query, (cpf,nome,email,login,senha,id,))
        db.commit()
        
        return redirect(url_for('cadastrar_funcionarios'))
    
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

# Atualizar Disciplina
@app.route('/updateDisciplina/<int:id>', methods=['GET'])
def updateDisciplina(id):    

    select_query = "SELECT * FROM ze_TB_disciplina WHERE id = %s"
    mycursor.execute(select_query, (id,))
    disciplina = mycursor.fetchone()

    return render_template('atualizar_disciplina.html', disciplina = disciplina)

@app.route('/updateDisciplina', methods=['POST'])
def update_diciplina():
    if request.method == 'POST':

        id = request.form['id']
        disciplina = request.form['disciplina']

        select_query = "UPDATE ze_TB_disciplina SET disciplina = %s WHERE id = %s"
        mycursor.execute(select_query, (disciplina,id,))
        db.commit()
        
        return redirect(url_for('cadastrar_disciplinas'))
    
    return render_template('atualizar_disicplina.html')

#Excluir Disciplina
@app.route('/deleteDisciplina/<disciplina>',methods=['GET'])
def deleteDisciplina(disciplina):
   
   queryVerificadora = "SELECT * FROM ze_TB_notas WHERE id_Materia = %s"
   mycursor.execute(queryVerificadora, (disciplina,))
   alunosCad = mycursor.fetchone()[0]
   
   if alunosCad > 0:
     message = "A Disciplina está associada a pelo menos um aluno, não é possível excluí-la."
     return render_template('cadastrar_disciplinas.html',message = message)
   
   select_query = "DELETE from ze_TB_disciplina where id = %s"
   mycursor.execute(select_query,(disciplina,))
   db.commit()

   return redirect(url_for('cadastrar_disciplinas'))

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

       
        select_query2 = ('SELECT idNotas, a.nome, m.disciplina, n.nota1, n.nota2, n.nota3, n.nota4 FROM ze_TB_notas n INNER JOIN ze_TB_disciplina m ON n.id_Materia = m.id INNER JOIN ze_TB_alunos a ON n.id_Aluno = a.id')
        mycursor.execute(select_query2)
        nota = mycursor.fetchall()
        



        return render_template('cadastrar_notas.html', alunos = aluno, materias = materia ,notas = nota)
    
    if request.method == 'POST':

        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])
        nota4 = float(request.form['nota4'])
        media = round((nota1 + nota2 + nota3 + nota4)/4,2)
        idAluno = request.form.get('selectAluno')
        idMateria = request.form.get('selectMateria')

        select_query = 'INSERT INTO ze_TB_notas (id_Aluno,id_Materia,nota1,nota2,nota3,nota4,media) VALUES (%s,%s,%s,%s,%s,%s,%s)'

        mycursor.execute(select_query,(idAluno,idMateria,nota1,nota2,nota3,nota4,media))
        db.commit()

        return redirect(url_for('cadastrar_notas'))
    
    return render_template('cadastrar_notas.html')

#Excluir Nota
@app.route('/deleteNotas/<nota>')
def deleteNota(nota):
   select_query = "DELETE from ze_TB_nota where id = '" + nota + "'"
   print(select_query)
   mycursor.execute(select_query)
   db.commit()
   return redirect(url_for('cadastrar_notas'))

#Atualizar Notas
@app.route('/updateNotas/<int:idNotas>', methods=['GET'])
def updateNotas(idNotas):    

    select_query = "SELECT * FROM ze_TB_notas WHERE idNotas = %s"
    mycursor.execute(select_query, (idNotas,))
    notas = mycursor.fetchone()

    return render_template('atualizar_notas.html', notas = notas)

@app.route('/updateNotas', methods=['POST'])
def update_notas():
    if request.method == 'POST':

        idNotas = request.form.get('idNotas')
        idAluno = request.form['idAluno']
        idMateria = request.form['idMateria']
        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])
        nota4 = float(request.form['nota4'])
        media = round((nota1 + nota2 + nota3 + nota4)/4,2)

        select_query = "UPDATE ze_TB_notas SET id_Aluno = %s, id_Materia = %s, nota1 = %s, nota2 = %s, nota3 = %s, nota4 = %s, media = %s WHERE idNotas = %s"
        mycursor.execute(select_query, (idAluno,idMateria,nota1,nota2,nota3,nota4,media,idNotas,))
        db.commit()
        
        return redirect(url_for('cadastrar_notas'))
    
    return render_template('atualizar_notas.html')

if __name__ == '__main__':
    app.run(debug=True)