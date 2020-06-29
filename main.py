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
    description = db.Column(db.String(500))
    point_value = db.Column(db.Integer)
    def __init__(self, name, description, point_value):
        self.name = name
        self.description = description
        self.point_value = point_value

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(16))
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    def __init__(self, title):
        self.title = title


@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()


@app.route("/signup", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

   
    template = jinja_env.get_template('signup.html')
    return template.render()

@app.route('/add-tasks', methods=['POST', 'GET'])
def add_tasks():

    if request.method == 'POST':
        task_name = request.form['task']
        task_description = request.form['task_description']
        task_point_value = request.form['task_point_value']
        new_task = Task(task_name, task_description, int(task_point_value))
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()

    template = jinja_env.get_template('add-tasks.html')
    return template.render(title="add-tasks", tasks=tasks)

@app.route("/my-tasks", methods=['GET'])
def display_my_tasks():
    template = jinja_env.get_template('my-tasks.html')
    tasks = Task.query.all()
    return template.render(title="my-tasks", tasks=tasks)


@app.route('/task-completed', methods=['POST'])
def display_task_submitted():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    point_value = task.point_value
    #print(task)
    template = jinja_env.get_template('task-completed.html')

    return template.render(task=task, point_value=point_value)


if __name__ == '__main__':
    app.run()