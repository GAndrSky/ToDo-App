from email.policy import default

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200), nullable = False)
    status = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list = todo_list)

@app.route('/add', methods = ['POST'])
def add():
    task = request.form['task']
    new_task = Todo(task = task)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)
