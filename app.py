from datetime import datetime
from flask import Flask, render_template, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy

# database 생성 코드
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

# Todo Table
class Todo(db.Model):
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/todos/<int:todoId>', methods=['DELETE'])
def delete_todo_by_id(todoId):
    todo = Todo.query.filter_by(list_id = todoId).first()

    if todo is None:
        return jsonify({"error" : f"Todo with id {todoId} not found"}), 404
    else:
        db.session.delete(todo)
        db.session.commit()

    return jsonify({"message" : f"Todo with id {todoId} deleted successfully"}), 200

@app.route('/api/todos/<int:todoId>', methods=['PATCH'])
def update_todo_by_id(todoId):
    data = request.get_json()

    request_completed = data.get('completed')
    request_contents = data.get('contents')

    todo = Todo.query.filter_by(list_id = todoId).first()
    if todo is None:
        return jsonify({"error" : f"Todo with id {todoId} not found"}), 404
    else:
        todo.contents = request_contents
        todo.completed = request_completed
        db.session.add(todo)
        db.session.commit()

    return jsonify({"message" : f"Todo with id {todoId} updated successfully"}), 200

#

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/api/todos/<string:username>/<string:date>', methods=['GET'])
def load_todo_by_date(date, username):
    # date를 datetime 객체로 변환
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    todos = Todo.query.filter_by(created_at=date_obj, username=username).all()
    if not todos: # todos가 빈 리스트인 경우
        return jsonify({"error" : f"Todo was created at {date} not found"}), 404
    
    todo_list = []
    for todo in todos:
        todo_list.append({
            "list_id" : todo.list_id,
            "contents" : todo.contents,
            "completed" : todo.completed
        })

    return jsonify({"message" : f"Todo with the date {date} successfully found",
                    "todo_list" : todo_list}), 200

@app.route('/api/todos/', methods=['POST'])
def create_todo():
    data = request.get_json()

    request_username = data.get('username')
    request_contents = data.get('contents')
    request_created_at = data.get('created_at')
    request_completed = data.get('completed')
    
    print(request_username)

    try:
        date_created_at = datetime.strptime(request_created_at, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error" : "Invalid date format"}), 400

    todo = Todo(username=request_username, contents=request_contents, created_at=date_created_at, completed=request_completed)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message" : "Create Todo Successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)