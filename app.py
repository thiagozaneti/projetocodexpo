from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required

app = Flask(__name__)

app.static_url_path = 'static'
app.static_folder = 'static'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:5e51#123@localhost/projeto"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ttttgg,x>a({&(5oqffx,`@>w[]pmifi|]#{6?q60ov#h~@wr>nyl,@,p{:g|;?u>0|ltttt'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

@login_manager.user_loader    #A função load_user é usada pelo Flask-Login para carregar um objeto de usuário com base no user_id armazenado na sessão do usuário. Isso permite que o Flask-Login mantenha o controle da sessão do usuário.
def load_user(user_id):
    return User.query.get(int(user_id))

##visualização inicial do usuário
@app.route('/')
def index(): 
    return render_template('home.html')

##rota de registro
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
    return render_template('register.html')

##rota de login
@app.route('/login')
def login():
    return render_template('login.html')


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