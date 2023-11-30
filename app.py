from flask import Flask, render_template, request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user

app = Flask(__name__)

app.static_url_path = 'static'
app.static_folder = 'static'
admin = Admin(app, name='Admin')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:5e5i#123@localhost/projeto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ttttgg,x>a({&(5oqffx,`@>w[]pmifi|]#{6?q60ov#h~@wr>nyl,@,p{:g|;?u>0|ltttt'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin): 
    __tablename__ = "inscricoes"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    
class Empregados(db.Model, UserMixin): 
    __tablename__ = 'empregados'
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
    password = db.Column(db.String(50), nullable=False)  # Make sure this line is present
    funcao = db.Column(db.String(50), nullable=False)
    senhaAdm = db.Column(db.String(50), nullable=False)

admin.add_view(ModelView(User, db.session))




class Buy(db.Model, UserMixin):
    __tablename__ = 'info_users_buy'
    id = db.Column(db.Integer, primary_key=True)
    number_card = db.Column(db.String(200), nullable=False)
    date_expires = db.Column(db.String(200), nullable=False)
    cvv = db.Column(db.String(200), nullable=False)
    name_of_propriety = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    selecao = db.Column(db.String(200), nullable=False)



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
        if len(password) <= 4:
            message = "Senha fraca"
        elif len(email) <= 5:
            message = "E-mail fraco"
        elif len(username) <= 4:
            message = "Nome de usuário fraco"
        elif len(username) > 20:
            message = "Usuário excedente, mínimo 20 caracteres"
        else:
            new_user = User(username=username, email=email, password=password)
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
        user = User.query.filter_by(email=email, password=password).first()
        admin_user = Admin.query.filter_by(email=email, password=password).first()  # Rename admin to admin_user
        
        if user:
            login_user(user)
            return redirect(url_for('system'))
        if admin_user:
            login_user(admin_user)
            return redirect(url_for('admin'))
        else:
            message = "Usuário não encontrado, tente novamente"
            return redirect(url_for('index'))
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
    return render_template('system/systemUser.html')

@app.route('/system_Buy', methods = ['POST','GET'])
@login_required
def systemBuy():
    if request.method == 'POST':
        number_card = request.form.get('number_card')
        date_expires = request.form.get('date_expires')
        cvv = request.form.get('cvv')
        name_of_propriety = request.form.get('name_of_propriety')
        email = request.form.get('email')


        new_buy = Buy(number_card = number_card, date_expires = date_expires, cvv = cvv, name_of_propriety = name_of_propriety, email = email)
        db.session.add(new_buy)
        db.session.commit()
    return render_template('system/systemBuy.html')


##<---------------------------------->

@app.route('/homeadm')
@login_required
def homeadm():
    username = current_user.username
    email = current_user.email
    return render_template('systemAdm/systemAdmHome.html', username=username, email=email)

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
    nome = request.args.get('nome')
    email = request.args.get('email')
    password = request.args.get('senha')
    funcao = request.args.get('funcaoadm')
    senhaAdm = request.args.get('senhaadm')
    lista_admin_add = Admin.query.filter_by(nome=nome, email=email, password=password, funcao=funcao, senhaAdm=senhaAdm).all()
    return render_template('systemAdm/systemadms.html', lista_admin_add = lista_admin_add)

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
            db.session.commit()
            message = 'usuário adicionado com sucesso'
            return redirect(url_for('systemadms', nome=nome, email = email, password = password, funcao = funcao, senhaAdm = senhaAdm))
        else:
            message = 'senha modelo errada, redirecionando, tente novamente'
            return redirect(url_for('systemadms'))
    return render_template('systemAdm/formsAdm/forms_add_admins.html', message = message)



@app.route('/system_adm_employer')
def systemadmemployer():
    return render_template('systemAdm/systemadmemployer.html')

@app.route('/system_add_employer', methods = ['POST', 'GET'] )
def system_add_employer():
    message = ''
    return render_template('systemAdm/formsAdm/forms_add_employers.html')

if __name__ == "__main__":
    app.run()
    login_manager.init_app(app)

##//TODO:DESENVOLVER TODOS OS CRUDS 
##//TODO:Desenvolver crud de empregados
##//TODO:TERMINAR VERIFICAÇÃO DO LOGIN DE USUÁRIO 
##//TODO:Desenvolver algoritmo random identificador 
##//TODO:Desenvolver sistema de email

