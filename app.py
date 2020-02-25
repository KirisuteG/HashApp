from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/database0.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    done = db.Column(db.Boolean)

@app.route('/chain', methods=['GET'])
def home():
    tasks = Task.query.all() 
    return render_template('index.html', tasks = tasks)


@app.route('/chain', methods=['POST'])
def create():
    task = Task(content=generate_password_hash(request.form['content']),done=False)  
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/chain/last', methods=['GET'])
def last():
    last = Task.query.all()
    return str(last[-1].content)

@app.route('/api/v1/chain/', methods=['GET'])
def json():
    return jsonify({'Json': Task.query.all()})

@app.route('/chain/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/chain/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)  
