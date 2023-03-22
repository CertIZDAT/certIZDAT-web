from flask import Flask, render_template

app = Flask(__name__, template_folder='../frontend/', static_folder='../frontend/', static_url_path='/frontend')


@app.route('/')
def index():
    return render_template('index.html')
