from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.static_url_path = 'static'
app.static_folder = 'static'


##visualização inicial do usuário
@app.route('/')
def index(): 
    return render_template('home.html')

##rota de registro
@app.route('/register')
def register():
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


if __name__ == "__main__":
    app.run()