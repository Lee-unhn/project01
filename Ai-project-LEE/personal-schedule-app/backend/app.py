import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Configure Database
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'schedule.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model ---
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=2)  # 1: High, 2: Medium, 3: Low
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': self.date.isoformat(),
            'time': self.time.isoformat() if self.time else None,
            'priority': self.priority,
            'completed': self.completed
        }

# --- API Endpoints ---
@app.route('/todos', methods=['GET'])
def get_todos():
    """
    Get todos, optionally filtered by a date range.
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    query = Todo.query

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        query = query.filter(Todo.date >= start_date)
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        query = query.filter(Todo.date <= end_date)

    todos = query.order_by(Todo.date, Todo.time).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    """
    Add a new todo item.
    """
    data = request.get_json()
    if not data or not data.get('content') or not data.get('date'):
        return jsonify({'error': 'Missing required fields'}), 400

    new_todo = Todo(
        content=data['content'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time=datetime.strptime(data['time'], '%H:%M').time() if data.get('time') else None,
        priority=data.get('priority', 2)
    )

    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    """
    Update an existing todo item.
    """
    todo = Todo.query.get_or_404(id)
    data = request.get_json()

    if 'content' in data:
        todo.content = data['content']
    if 'date' in data:
        todo.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'time' in data:
        todo.time = datetime.strptime(data['time'], '%H:%M').time() if data.get('time') else None
    if 'priority' in data:
        todo.priority = data['priority']
    if 'completed' in data:
        todo.completed = data['completed']

    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """
    Delete a todo item.
    """
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

# --- Main Execution ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
