# Introduction to Flask

## Table of Contents

- [What is Flask](#what-is-flask)
- [Installation](#installation)
- [Your First Flask App](#your-first-flask-app)
- [Routing](#routing)
- [Templates with Jinja2](#templates-with-jinja2)
- [Request and Response](#request-and-response)
- [Forms and Validation](#forms-and-validation)
- [Database Integration with Flask-SQLAlchemy](#database-integration-with-flask-sqlalchemy)
- [Blueprints](#blueprints)
- [Error Handling](#error-handling)
- [RESTful API Patterns](#restful-api-patterns)
- [Testing](#testing)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Flask

Flask is a lightweight WSGI web application framework for Python. It is classified as a microframework because it does not require particular tools or libraries beyond the standard library. Flask provides the essentials for building web applications while letting developers choose their own tools for databases, form validation, and other components.

Key characteristics:
- Minimal core with extension-based architecture
- Built-in development server and debugger
- Jinja2 template engine
- WSGI 1.0 compliant
- Extensive documentation and large community

---

## Installation

```python
# Install Flask using pip
# pip install flask

# Verify the installation
import flask
print(flask.__version__)  # prints the installed version

# Common additional packages
# pip install flask-sqlalchemy   # database ORM integration
# pip install flask-wtf          # form handling and CSRF protection
# pip install flask-login        # user session management
```

---

## Your First Flask App

```python
# app.py - A minimal Flask application
from flask import Flask

# Create a Flask application instance
# __name__ tells Flask where to find resources (templates, static files)
app = Flask(__name__)

# Define a route using a decorator
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/about")
def about():
    return "<h1>About Page</h1><p>This is my Flask app.</p>"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)  # debug=True enables auto-reload and interactive debugger

# Running from the command line:
# flask --app app run --debug
# flask --app app run --port 8080     # custom port
# flask --app app run --host 0.0.0.0  # listen on all interfaces
```

```python
# Application configuration
from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "my-secret-key"             # for session security
app.config["DEBUG"] = True                              # enable debug mode
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024    # 16 MB upload limit
```

---

## Routing

```python
from flask import Flask, request, url_for

app = Flask(__name__)

# Variable rules - capture parts of the URL
@app.route("/user/<username>")
def show_user_profile(username):
    return f"User: {username}"  # username is a string by default

# Type converters for URL variables
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post {post_id}"  # post_id is converted to an integer

# Available converters: string (default), int, float, path, uuid
@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath: {subpath}"  # path converter captures slashes

# Specifying allowed HTTP methods
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Processing login..."
    else:
        return "Show login form"

# Separate decorators for different methods
@app.get("/items")
def get_items():
    return "List of items"

@app.post("/items")
def create_item():
    return "Item created"

# URL building with url_for
@app.route("/")
def index():
    profile_url = url_for("show_user_profile", username="alice")
    # Returns: /user/alice
    return f'<a href="{profile_url}">Alice Profile</a>'

# Trailing slash behavior
@app.route("/projects/")
def projects():
    return "The project list"  # /projects redirects to /projects/

@app.route("/about")
def about():
    return "The about page"  # /about/ returns a 404
```

---

## Templates with Jinja2

```python
# Flask uses Jinja2 as its template engine
# Templates are stored in a "templates" directory by default

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="Home")

@app.route("/user/<name>")
def user(name):
    # Pass variables to the template as keyword arguments
    return render_template(
        "user.html",
        username=name,
        items=["apple", "banana", "cherry"]
    )
```

```python
# templates/base.html - Template inheritance base
# <!DOCTYPE html>
# <html>
# <head><title>{% block title %}My Site{% endblock %}</title></head>
# <body>
#     <nav>Navigation here</nav>
#     {% block content %}{% endblock %}
#     <footer>Footer here</footer>
# </body>
# </html>

# templates/index.html - Child template
# {% extends "base.html" %}
# {% block title %}Home{% endblock %}
# {% block content %}
#   <h1>Welcome, {{ username }}!</h1>
#   {% if items %}
#     <ul>
#       {% for item in items %}
#         <li>{{ loop.index }}. {{ item }}</li>
#       {% endfor %}
#     </ul>
#   {% else %}
#     <p>No items found.</p>
#   {% endif %}
# {% endblock %}

# Common Jinja2 features:
# Variables: {{ variable }}
# Filters:  {{ name|capitalize }}  {{ items|length }}
# Comments: {# This is a comment #}
# Loop vars: loop.index, loop.first, loop.last, loop.length
```

---

## Request and Response

```python
from flask import Flask, request, jsonify, redirect, url_for, make_response

app = Flask(__name__)

# Accessing request data
@app.route("/search")
def search():
    query = request.args.get("q", "")              # query parameter with default
    page = request.args.get("page", 1, type=int)   # type conversion
    return f"Searching for '{query}' on page {page}"

# Handling JSON request bodies
@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.get_json()               # parse JSON body
    name = data.get("name", "unknown")
    return jsonify({"received": name})       # return JSON response

# Accessing form data
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    return f"Received: {username}"

# Accessing headers and cookies
@app.route("/info")
def info():
    user_agent = request.headers.get("User-Agent")
    token = request.cookies.get("session_token")
    return jsonify({"user_agent": user_agent, "token": token})
```

```python
from flask import Flask, make_response, jsonify, redirect, url_for

app = Flask(__name__)

# Custom response with headers
@app.route("/custom")
def custom_response():
    response = make_response("Custom response body", 200)
    response.headers["X-Custom-Header"] = "my-value"
    return response

# Setting cookies
@app.route("/set-cookie")
def set_cookie():
    response = make_response("Cookie set!")
    response.set_cookie("user_id", "12345", max_age=3600, httponly=True)
    return response

# Redirects
@app.route("/old-page")
def old_page():
    return redirect(url_for("new_page"))  # 302 redirect

@app.route("/new-page")
def new_page():
    return "This is the new page"

# Returning JSON
@app.route("/api/users")
def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)  # sets Content-Type to application/json
```

---

## Forms and Validation

```python
# Using Flask-WTF for form handling
# pip install flask-wtf

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"  # required for CSRF protection

class RegistrationForm(FlaskForm):
    username = StringField("Username",
        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email",
        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
        validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Register")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Form data is valid
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)

# Template for register.html:
# <form method="POST">
#     {{ form.hidden_tag() }}     <!-- CSRF token -->
#     {{ form.username.label }}   {{ form.username() }}
#     {% for error in form.username.errors %}
#         <span class="error">{{ error }}</span>
#     {% endfor %}
#     {{ form.submit() }}
# </form>
```

---

## Database Integration with Flask-SQLAlchemy

```python
# pip install flask-sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author", lazy=True)  # one-to-many

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Create all tables
with app.app_context():
    db.create_all()
```

```python
# CRUD operations within routes
@app.route("/create-user")
def create_user():
    user = User(username="alice", email="alice@example.com")
    db.session.add(user)
    db.session.commit()
    return f"User {user.id} created"

@app.route("/users")
def list_users():
    users = User.query.all()                                    # get all
    by_id = User.query.get(1)                                   # by primary key
    filtered = User.query.filter_by(username="alice").first()   # filter
    paginated = User.query.paginate(page=1, per_page=10)        # pagination
    return f"Found {len(users)} users"

@app.route("/update-user/<int:user_id>")
def update_user(user_id):
    user = User.query.get_or_404(user_id)  # 404 if not found
    user.username = "alice_updated"
    db.session.commit()
    return f"User {user_id} updated"

@app.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return f"User {user_id} deleted"
```

---

## Blueprints

```python
# Blueprints organize a Flask app into modular components

# auth/routes.py
from flask import Blueprint, redirect, url_for

auth_bp = Blueprint(
    "auth", __name__,
    template_folder="templates",  # blueprint-specific templates
    url_prefix="/auth"            # all routes prefixed with /auth
)

@auth_bp.route("/login")
def login():
    return "Login Page"

@auth_bp.route("/register")
def register():
    return "Register Page"

# main/routes.py
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "Home Page"
```

```python
# myapp/__init__.py - Register blueprints with the app
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"

    from myapp.auth.routes import auth_bp
    from myapp.main.routes import main_bp

    app.register_blueprint(auth_bp)   # routes at /auth/login, /auth/register
    app.register_blueprint(main_bp)   # routes at /

    return app

# Using url_for with blueprints:
# url_for("auth.login")   -> /auth/login
# url_for("main.index")   -> /
```

---

## Error Handling

```python
from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)

# Custom error pages
@app.errorhandler(404)
def not_found(error):
    if request.accept_mimetypes.best == "application/json":
        return jsonify({"error": "Not found"}), 404
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

# Abort with a specific error code
@app.route("/admin")
def admin():
    is_admin = False
    if not is_admin:
        abort(403)  # raises a 403 Forbidden error
    return "Admin Panel"

# Custom exception handling
class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"error": error.message}), error.status_code
```

---

## RESTful API Patterns

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

books = [
    {"id": 1, "title": "Flask Web Development", "author": "Miguel Grinberg"},
    {"id": 2, "title": "Python Crash Course", "author": "Eric Matthes"},
]
next_id = 3

# GET /api/books - List all books
@app.route("/api/books", methods=["GET"])
def get_books():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start = (page - 1) * per_page
    return jsonify({"books": books[start:start + per_page], "total": len(books)})

# GET /api/books/<id> - Get a single book
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404)
    return jsonify(book)

# POST /api/books - Create a new book
@app.route("/api/books", methods=["POST"])
def create_book():
    global next_id
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        abort(400)
    book = {"id": next_id, "title": data["title"], "author": data["author"]}
    next_id += 1
    books.append(book)
    return jsonify(book), 201

# PUT /api/books/<id> - Update a book
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404)
    data = request.get_json()
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    return jsonify(book)

# DELETE /api/books/<id> - Delete a book
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404)
    books = [b for b in books if b["id"] != book_id]
    return "", 204
```

---

## Testing

```python
import pytest
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

@app.route("/api/data", methods=["POST"])
def create_data():
    from flask import request, jsonify
    data = request.get_json()
    return jsonify(data), 201

# Pytest fixtures for testing
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data

def test_create_data(client):
    response = client.post("/api/data", json={"name": "test"},
                           content_type="application/json")
    assert response.status_code == 201
    assert response.get_json()["name"] == "test"

def test_not_found(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
```

---

## Practice Exercises

1. **Personal Blog**: Build a simple blog with routes for listing posts, viewing a single post, and creating new posts using templates and forms.

2. **REST API**: Create a RESTful API for a task management system with CRUD operations, pagination, and filtering by status.

3. **User Authentication**: Implement user registration, login, and logout using Flask-Login and session management.

4. **Blueprint Refactor**: Take a monolithic Flask application and refactor it into blueprints for auth, API, and main page modules.

5. **Database CRUD**: Build a contact book application using Flask-SQLAlchemy with models for contacts and groups.

---

## Summary

Flask is a lightweight and flexible Python web framework that provides the essentials without imposing structure. Key takeaways:

- Flask uses decorators to map URL routes to Python functions
- Jinja2 templates support inheritance, control structures, and macros
- The request object provides access to query parameters, form data, JSON, headers, and cookies
- Flask-SQLAlchemy integrates SQLAlchemy ORM for database operations
- Blueprints enable modular application organization
- Flask-WTF handles form rendering, validation, and CSRF protection
- The built-in test client allows testing without a running server
- Error handlers can return different formats (HTML vs JSON) based on the request

---

## Next Steps

- Learn Flask-Migrate for database schema migrations
- Explore Flask-Login for user session management
- Study Flask-RESTful or Flask-Smorest for structured API development
- Investigate Flask-Caching for performance optimization
- Look into deployment with Gunicorn and Nginx

---

## Additional Resources

- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Flask GitHub Repository](https://github.com/pallets/flask)
- [Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Real Python Flask Tutorials](https://realpython.com/tutorials/flask/)
