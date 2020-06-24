from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dz-app:password@localhost:8889/dz-app'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    def __init__(self, name):
        self.name = name

@app.route("/")
def index():
    template = jinja_env.get_template('hello_form.html')
    return template.render()


@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form['first_name']
    template = jinja_env.get_template('hello_display.html')
    return template.render(name=first_name)


tasks = []

@app.route('/todos', methods=['POST', 'GET'])
def todos():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    template = jinja_env.get_template('todos.html')
    return template.render(title="TODOS", tasks=tasks)

@app.route("/inputs", methods=['GET'])
def inputs():
    template = jinja_env.get_template('inputs.html')
    return template.render()


@app.route('/validate-time')
def display_time_form():
    template = jinja_env.get_template('time_form.html')
    return template.render()


if __name__ == '__main__':
    app.run()