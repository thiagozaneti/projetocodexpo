from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.static_url_path = 'static'
app.static_folder = 'static'



@app.route('/')
def index(): 
    return render_template('home.html')

if __name__ == "__main__":
    app.run()