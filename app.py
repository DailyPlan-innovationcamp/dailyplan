from flask import Flask, render_template
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
    list_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)