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

class User(db.Model, UserMixin): 
    __tablename__ = "inscricoes"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

admin.add_view(ModelView(User, db.session))



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
    return render_template('home.html')

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
    return render_template('register.html')

##rota de login
@app.route("/login", methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')
        user = User.query.filter_by(email=email, password=password).first()
        admin = Admin.query.filter_by(email = email, password = password).first()
        if user:
            login_user(user) #quando é autenticado, o flask cria uma sessao de usuario adequeda, mantendo o usuario autenticado
            return redirect(url_for('system'))
        elif admin:
            login_user(admin)
            return redirect(url_for('admin'))
        else:
            message = "Usuário não encontrado, tente novamente"
            return redirect(url_for('index'))
    return render_template('login.html')

##rota do adm
@app.route('/admin')
def admin():
    return render_template('systemAdm/systemAdmHome.html')

##Acesso a sistema do usuário / venda de ingresso
@app.route('/system')
def system():
    return render_template('system/system.html')

##Acesso ao sistema na secao de usuario de eventos
@app.route('/systemEvent')
def systemNotices():
    return render_template('system/systemEvent.html')

##Acesso ao sistema na secao de usuario de shop
@app.route('/systemShop')
def systemShop():
    return render_template('system/systemShop.html')

@app.route('/systemBuy')
def systemBuy():
    return render_template('system/systemBuy.html')


if __name__ == "__main__":
    app.run()