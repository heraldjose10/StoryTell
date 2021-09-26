from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfuygiaughdauij3q72846yqiuehrgiq'

from blogApp import routes