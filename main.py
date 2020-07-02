from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

#To do:
#Add Points to User class so each user can have cumulative points for the tasks they complete
#Make one to many relationship with Users to Tasks
#User signs up and it walked them through the process of adding goals and associated tasks
#Make many to many relationship of tasks to goals.  One task may help move you towards two or more goals, so points can go into both categories


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dz-app:password@localhost:8889/dz-app'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(500))
    point_value = db.Column(db.Integer, default=0)
    def __init__(self, name, description, point_value):
        self.name = name
        self.description = description
        self.point_value = point_value

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(16))
    points = db.Column(db.Integer)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(300))
    def __init__(self, title):
        self.title = title

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and'email' not in session:
        return redirect('/login')


@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        template = jinja_env.get_template('register.html')
        return template.render()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        
        if password == verify and not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            
            return redirect('/')
        else:
            error = 'passwords did not match and/or that username is already taken'
            template = jinja_env.get_template('register.html')
            return template.render(error=error)
            #redirect('/register', error=error)
   
   # template = jinja_env.get_template('register.html')
    #return template.render()


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/')
        else:
            # TO DO - explain why login failed
            pass

    template = jinja_env.get_template('login.html')
    return template.render()

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')


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