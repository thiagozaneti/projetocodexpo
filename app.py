from flask import Flask, render_template, request, redirect, url_for, session
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
import random
import string
import time


app = Flask(__name__)

app.static_url_path = 'static'
app.static_folder = 'static'
admin = Admin(app, name='Admin')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:5e5i#123@localhost/projeto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ttttgg,x>a({&(5oqffx,`@>w[]pmifi|]#{6?q60ov#h~@wr>nyl,@,p{:g|;?u>0|ltttt'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin): 
    __tablename__ = "inscricoes"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    
class Empregados(db.Model, UserMixin): 
    __tablename__ = 'Empregados'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    selecao_empregados = db.Column(db.String(200), nullable=False)
    indicacao = db.Column(db.String(200), nullable=False)
    salario = db.Column(db.String(10), nullable=False)
    idade = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    tipo_de_servico = db.Column(db.String(200), nullable=False)
    inicio_trabalho = db.Column(db.String(10), nullable=False)
    fim_trabalho = db.Column(db.String(10), nullable=False)
    senha = db.Column(db.String(10), nullable=False)
    identificador = db.Column(db.String(5), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)  
    funcao = db.Column(db.String(50), nullable=False)
    senhaAdm = db.Column(db.String(50), nullable=False)
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

admin.add_view(ModelView(User, db.session))

class Buy(db.Model, UserMixin):
    __tablename__ = 'info_users_buy'
    id = db.Column(db.Integer, primary_key=True)
    number_card = db.Column(db.String(4), nullable=False)
    date_expires = db.Column(db.String(4), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    name_of_propriety = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    selecao = db.Column(db.String(200), nullable=False)
    sequencia = db.Column(db.String(8), nullable=False)


@login_manager.user_loader    #A função load_user é usada pelo Flask-Login para carregar um objeto de usuário com base no user_id armazenado na sessão do usuário. Isso permite que o Flask-Login mantenha o controle da sessão do usuário.
def load_user(user_id):
    return User.query.get(int(user_id))

##visualização inicial do usuário
@app.route('/')
def index(): 
    return render_template('home.html')

@app.route('/sair')
def exit():
    logout_user()
    return redirect(url_for('index'))

##rota de registro
@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('senha')
        if len(username) < 3:
            return redirect('register')
        elif len(username) > 30:
            return redirect('register')
        elif len(password) < 6:
            return redirect('register')
        elif len(password) > 16:
            return redirect('register')
        else:
            new_user = User(username=username, email=email, password=password)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            message = 'Cadastro feito com sucesso'
            return redirect(url_for('login'))
    return render_template('register.html', message = message)

##rota de login
@app.route("/login", methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')
        user = User.query.filter_by(email=email).first()
        admin_user = Admin.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if 4 <= len(password) <= 16:  # Verifica o comprimento da senha
                login_user(user)
                return redirect(url_for('system'))
            else:
                message = 'A senha deve ter entre 4 e 16 caracteres'
        elif admin_user and admin_user.check_password(password):
            login_user(admin_user)
            return redirect(url_for('admin'))
        else:
            message = "Usuário não encontrado ou senha incorreta, tente novamente"

    return render_template('login.html', message=message)



   
##rota do adm
@app.route('/admin')
def admin():
    return render_template('systemAdm/systemAdmHome.html')


##Acesso a sistema do usuário / venda de ingresso
@app.route('/system')
@login_required
def system():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    return render_template('system/system.html')

##Acesso ao sistema na secao de usuario de eventos
@app.route('/system_Event')
@login_required
def systemNotices():
    return render_template('system/systemEvent.html')

##Acesso ao sistema na secao de usuario de shop
@app.route('/system_Shop')
@login_required
def systemShop():
    return render_template('system/systemShop.html')

@app.route('/system_profile')
@login_required
def system_profile():
    username = current_user.username
    email = current_user.email
    nova_sequencia = session.get('nova_sequencia')
    return render_template('system/systemUser.html', nova_sequencia = nova_sequencia, username = username, email = email)

@app.route('/system_buy', methods = ['POST','GET'])
@login_required
def systemBuy():
    message = ''
    if request.method == 'POST':
        number_card = request.form.get('number_card')
        date_expires = request.form.get('date_expires')
        cvv = request.form.get('cvv')
        name_of_propriety = request.form.get('name_of_propriety')
        selecao = request.form.get('selecao')
        email = request.form.get('email')
        if len(str(number_card)) != 4:
            message = 'Numero de cartao errado'
        if len(date_expires) !=4:
            message = 'Numero de fim errado'
        elif len(cvv) !=3:
            message = 'Cvv errado'
        elif len(str(number_card)) != 16 and len(date_expires) !=4 and len(cvv) !=3:
            message = 'Todos os campos possuem poucos caracteres'
        else:
        ##algoritmo gerador de sequencia
            nova_sequencia = ''.join(random.choices(string.ascii_uppercase+ string.digits, k=8))
            session['nova_sequencia'] = nova_sequencia ## armazena variaveis em lista que recebem a variavel para a sessao do usuário
            ##fim do algoritmo
            new_buy = Buy(number_card = number_card, date_expires = date_expires, cvv = cvv, name_of_propriety = name_of_propriety, email = email, selecao = selecao, sequencia = nova_sequencia)
            db.session.add(new_buy)
            db.session.commit()
            time.sleep(5)
            message = 'Compra realizada com sucesso! Você sõ pode comprar apenas um ingresso por seção'
            return redirect(url_for('systemBuy', nova_sequencia = nova_sequencia) )
    return render_template('system/systemBuy.html', message = message)


##<---------------------------------->

@app.route('/homeadm')
def homeadm():
    total_ingressos = Buy.query.count()
    valor_todos_ingressos = db.session.query(func.sum(Buy.selecao)).scalar() or 0
    total_users = User.query.count()
    total_administradores = Admin.query.count()
    total_colaboradores = Empregados.query.count()
    username = None
    email = None
    if current_user.is_authenticated:
        username = current_user.username
        email = current_user.email
    return render_template('systemAdm/systemAdmHome.html',total_administradores = total_administradores, total_colaboradores = total_colaboradores, username = username, email=email, total_ingressos = total_ingressos, total_users = total_users, valor_todos_ingressos = valor_todos_ingressos)

@app.route('/system_adm_insc')
def systemadminsc():
    users = User.query.all()
    return render_template('systemAdm/systemadminsc.html', users = users)

@app.route('/delete_inscricao/<int:id>') ##deletar rota na rota -- usar para fazer as outras
def deleteInscricao(id):
    inscricao = User.query.get(id)
    
    if inscricao:
        db.session.delete(inscricao)
        db.session.commit()

    return redirect(url_for('systemadminsc'))

##<-------------------------------------------->




@app.route('/system_admin_ingressos')
def systemadminingressos():
    buy = Buy.query.all()
    return render_template('systemAdm/systemadminingressos.html', buy = buy)

@app.route('/delete_ingresso/<int:id>') ##deletar rota na rota -- usar para fazer as outras
def deleteIngresso(id):
    ingresso = Buy.query.get(id)
    
    if ingresso:
        db.session.delete(ingresso)
        db.session.commit()

    return redirect(url_for('systemadminingressos'))


##<------------------------------------------>
@app.route('/system_adm_compras')
def systemadmcompras():
    return render_template('systemAdm/systemadmcompras.html')

##<------------------------------------------>

@app.route('/system_adms')
def systemadms():
   lista = Admin.query.all()
   return render_template('systemAdm/systemadms.html', lista = lista )

##forms de adicão de adm / rota
@app.route('/add_admin', methods = ['POST','GET'])
def addAdmin():
    message = ''
    passwordModel = 'admin'
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('senha')
        funcao = request.form.get('funcaoadm')
        senhaAdm = request.form.get('senhaadm')
        if senhaAdm == passwordModel:
            adminAddBd = Admin(nome = nome, email = email, password = password, funcao = funcao, senhaAdm = senhaAdm)
            db.session.add(adminAddBd)
            adminAddBd.set_password(password)
            db.session.commit()
            message = 'usuário adicionado com sucesso'
            return redirect(url_for('systemadms', nome=nome, email = email, password = password, funcao = funcao, senhaAdm = senhaAdm))
        else:
            message = 'senha modelo errada, redirecionando, tente novamente'
            return redirect(url_for('systemadms'))
    return render_template('systemAdm/formsAdm/forms_add_admins.html', message = message)

@app.route('/delete_admin/<int:id>')
def delete_admin(id):
    administrador = Admin.query.get(id)
    
    if administrador:
        db.session.delete(administrador)
        db.session.commit()

    return redirect(url_for('systemadms'))

@app.route('/system_adm_employer')
def systemadmemployer():
    empregados = Empregados.query.all()
    return render_template('systemAdm/systemadmemployer.html', empregados = empregados)

@app.route('/system_add_employer', methods = ['POST', 'GET'] )
def system_add_employer():
    message = ''
    if request.method == 'POST':
        message = ''
    if request.method == 'POST':
        nome = request.form.get('nome')
        selecao_empregados = request.form.get('selecao_empregados')
        indicacao = request.form.get('indicacao')
        salario = request.form.get('salario')
        idade = request.form.get('idade')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        tipo_de_servico = request.form.get('tipo_de_servico')
        inicio_trabalho = request.form.get('inicio_trabalho')
        fim_trabalho = request.form.get('fim_trabalho')
        senha = request.form.get('senha')
        identificador = request.form.get('identificador')
        descricao = request.form.get('descricao')
        add_empregado = Empregados(nome = nome, selecao_empregados = selecao_empregados, indicacao = indicacao, salario = salario, idade = idade, telefone = telefone, email = email, tipo_de_servico = tipo_de_servico, inicio_trabalho = inicio_trabalho, fim_trabalho = fim_trabalho, senha = senha, identificador = identificador, descricao = descricao)
        db.session.add(add_empregado)
        db.session.commit()
        message = 'empregado adicionado com sucesso'
        return redirect(url_for('systemadmemployer'))
    return render_template('systemAdm/formsAdm/forms_add_employers.html')

@app.route('/delete_employer/<int:id>')
def delete_employer(id):
    colaborador = Empregados.query.get(id)
    
    if colaborador:
        db.session.delete(colaborador)
        db.session.commit()

    return redirect(url_for('systemadmemployer'))

if __name__ == "__main__":
    app.run()
    login_manager.init_app(app)


##//TODO:Desenvolver sistema de email
##//TODO:Deletar admin