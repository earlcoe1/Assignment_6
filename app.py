from flask import Flask, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -----------------------------
# Student Model
# -----------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)


# -----------------------------
# Book Model
# -----------------------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))


# Create database tables
with app.app_context():
    db.create_all()


# -----------------------------
# Lab 1: Student Records
# -----------------------------
@app.route('/')
def home():
    students = Student.query.all()

    return {
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "course": s.course
            }
            for s in students
        ]
    }


@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    course = request.form['course']

    new_student = Student(name=name, course=course)

    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)

    if student is None:
        return {"message": "Student not found"}, 404

    db.session.delete(student)
    db.session.commit()

    return {"message": "Student deleted successfully"}


# -----------------------------
# Lab 2: REST API Book Management
# -----------------------------
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "author": b.author
        }
        for b in books
    ])


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author']
    )

    db.session.add(new_book)
    db.session.commit()

    return {"message": "Book added"}


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if book is None:
        return {"message": "Book not found"}, 404

    db.session.delete(book)
    db.session.commit()

    return {"message": "Deleted"}


# -----------------------------
# Lab 3: GET Calculator App
# -----------------------------
@app.route('/calculator')
def calculator():
    return """
    <h2>Simple Calculator Using GET Method</h2>

    <form action="/calc" method="GET">
        <label>First Number:</label>
        <input type="number" name="num1" required><br><br>

        <label>Second Number:</label>
        <input type="number" name="num2" required><br><br>

        <label>Operation:</label>
        <select name="operation">
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
        </select><br><br>

        <button type="submit">Calculate</button>
    </form>
    """


@app.route('/calc', methods=['GET'])
def calc():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    operation = request.args.get('operation')

    if operation == 'add':
        result = num1 + num2
        symbol = "+"
    elif operation == 'subtract':
        result = num1 - num2
        symbol = "-"
    elif operation == 'multiply':
        result = num1 * num2
        symbol = "×"
    else:
        return "Invalid operation"

    return f"""
    <h2>Calculation Result</h2>
    <p>{num1} {symbol} {num2} = <strong>{result}</strong></p>
    <a href="/calculator">Go Back</a>
    """


if __name__ == '__main__':
    app.run(debug=True)
