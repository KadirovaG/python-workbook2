# Flask — Quick Start with uv

---

## What is a Library?

A **library** (also called a **package**) is code that someone else wrote so you don't have to. Instead of building everything from scratch, you install a library and use its ready-made functions and classes.

You already use libraries:

```python
import math          # math library — comes with Python
import random        # random library — comes with Python
```

Some libraries **don't** come with Python. They are created by other developers and shared online. You need to **install** them first. Flask is one of these.

---

## What is Flask?

**Flask** is a Python library for building **web applications** — websites, APIs, web services.

When you visit a website like `google.com`, your browser sends a request to a server. The server runs some code and sends back HTML (a web page) or JSON (data). Flask is the tool that lets you write that server code in Python.

```
Browser  -->  Request (URL)  -->  Flask app (Python)  -->  Response (HTML/JSON)  -->  Browser
```

Flask is called a **micro-framework** — it gives you just the essentials without unnecessary complexity. It's one of the most popular Python web frameworks, used by companies like Netflix, Reddit, and Lyft.

---

## What is uv?

**uv** is a modern Python project manager. It replaces multiple old tools at once:

```
Old way (3 separate tools):          New way (just uv):
  python -m venv .venv                 uv init
  source .venv/bin/activate            uv add flask
  pip install flask                    uv run app.py
  pip freeze > requirements.txt
  python app.py
```

`uv` does everything: creates the project, manages dependencies, runs your code — all in one tool, and it's extremely fast.

---

## Step 1 — Create a Project

```bash
mkdir my_flask_app
cd my_flask_app
uv init
```

`uv init` creates the project structure:

```
my_flask_app/
    .python-version      # which Python version to use
    pyproject.toml       # project settings + list of dependencies
    hello.py             # starter file (you can delete this)
```

`pyproject.toml` is like a recipe card for your project — it lists everything your project needs to run. `uv` manages this file automatically.

---

## Step 2 — Install Flask

```bash
uv add flask
```

This does three things:
1. Downloads Flask from the internet
2. Installs it in your project's environment
3. Adds it to `pyproject.toml` so anyone else can install the same dependencies

No `pip install`, no `venv`, no `requirements.txt`. One command.

---

## Step 3 — Write Your First App

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return "This is the about page"


if __name__ == "__main__":
    app.run(debug=True)
```

Let's break this down line by line:

```python
from flask import Flask       # import the Flask class from the flask library
```

```python
app = Flask(__name__)         # create a Flask application object
                              # __name__ tells Flask where your project lives
                              # (it's a built-in Python variable = current module name)
```

```python
@app.route("/")               # this is a decorator (explained below)
def home():                   # a regular Python function
    return "Hello, World!"    # what gets sent back to the browser
```

```python
app.run(debug=True)           # start the web server
                              # debug=True means: restart automatically when you change code
                              #                   show detailed errors in the browser
```

---

## Step 4 — Run It

```bash
uv run app.py
```

`uv run` = "run this file using the project's environment with all installed libraries."

If you used just `python app.py`, Python might not find Flask because it's installed in the project's environment, not globally.

Open your browser and go to: `http://127.0.0.1:5000`

`127.0.0.1` = your own computer (also called `localhost`). `:5000` = the port number Flask uses by default.

You should see: **Hello, World!**

Try: `http://127.0.0.1:5000/about` — you'll see "This is the about page."

---

## What is a Route?

A **route** is a connection between a **URL** and a **Python function**.

When someone visits a URL, Flask looks for a matching route and runs the corresponding function. The function's return value is sent back to the browser.

```
URL visited            Route          Function called     Browser shows
─────────────         ──────          ───────────────     ─────────────
localhost:5000/       "/"             home()              "Hello, World!"
localhost:5000/about  "/about"        about()             "This is the about page"
localhost:5000/xyz    no match        —                   404 Not Found
```

Think of routes like a phone menu:
- Press 1 for Sales → connects you to the Sales department
- Press 2 for Support → connects you to the Support department
- Visit `/` → runs the `home()` function
- Visit `/about` → runs the `about()` function

---

## What is a Decorator? What is `@app.route`?

### Decorators in General

A **decorator** is a special Python syntax that **modifies or extends** a function. It starts with `@` and goes right above a function definition.

```python
@something
def my_function():
    ...
```

This is equivalent to:

```python
def my_function():
    ...
my_function = something(my_function)
```

The decorator takes your function, wraps it with extra behavior, and gives it back. You've seen this before with `@property` in classes — it takes a method and turns it into something that behaves like an attribute.

### `@app.route` Specifically

`@app.route("/path")` is Flask's decorator. It does one thing: **registers your function as a handler for a specific URL**.

```python
@app.route("/")           # tells Flask: "when someone visits /, run this function"
def home():
    return "Hello, World!"
```

Without the decorator, Flask wouldn't know which function to call for which URL. The decorator is the glue between URLs and your Python code.

```python
@app.route("/about")      # URL: localhost:5000/about  -> calls about()
def about():
    return "About page"

@app.route("/contact")    # URL: localhost:5000/contact -> calls contact()
def contact():
    return "Contact page"

@app.route("/help")       # URL: localhost:5000/help    -> calls help_page()
def help_page():
    return "Help page"
```

Each `@app.route` registers one URL. One function per route, one route per function.

---

## Dynamic Routes — URLs with Variables

Sometimes you want a URL that changes. Instead of creating a separate route for every student, you create one route with a **variable**:

```python
@app.route("/student/<name>")
def student(name):
    return f"Hello, {name}!"
```

`<name>` is a placeholder. Whatever the user types in the URL gets passed to the function as the `name` parameter.

```
localhost:5000/student/Timur    -> name="Timur"    -> "Hello, Timur!"
localhost:5000/student/Shahrom  -> name="Shahrom"  -> "Hello, Shahrom!"
localhost:5000/student/Nizar    -> name="Nizar"    -> "Hello, Nizar!"
```

Important: the name inside `< >` in the route **must match** the function parameter name. `<name>` in the route = `name` in `def student(name)`.

You can also specify the type of the variable:

```python
@app.route("/grade/<name>/<int:score>")
def grade(name, score):
    if score >= 80:
        result = "Excellent"
    elif score >= 50:
        result = "Good"
    else:
        result = "Needs practice"
    return f"{name}: {score}% — {result}"

# localhost:5000/grade/Timur/89       -> Timur: 89% — Excellent
# localhost:5000/grade/Maftunbek/39   -> Maftunbek: 39% — Needs practice
```

`<int:score>` means "this part of the URL must be an integer." Flask will automatically convert the string `"89"` to the integer `89`.

Available types: `string` (default), `int`, `float`, `path`.

---

## Returning HTML

So far we returned plain text. But browsers understand **HTML** — the language of web pages. You can return HTML directly:

```python
@app.route("/")
def home():
    return """
    <html>
    <head><title>My App</title></head>
    <body>
        <h1>Welcome to Flask</h1>
        <p>This is HTML returned from Python</p>
        <a href="/about">Go to About</a>
    </body>
    </html>
    """
```

This works, but writing HTML inside Python strings gets messy fast. That's why Flask has **templates**.

---

## What are Templates?

A **template** is an HTML file with placeholders for dynamic data. Flask uses a template engine called **Jinja2** (installed automatically with Flask).

Instead of mixing HTML and Python, you keep them separate:
- Python handles the logic and data
- HTML templates handle the presentation

Create a folder called `templates/` (Flask looks for this exact name):

```
my_flask_app/
    app.py
    templates/
        home.html
```

`templates/home.html`:

```html
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
    {% for student in students %}
        <li>{{ student }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    names = ["Timur", "Shahrom", "Nizar", "Behruz", "Ahmadjon"]
    return render_template("home.html", title="Our Class", students=names)


if __name__ == "__main__":
    app.run(debug=True)
```

`render_template("home.html", title="Our Class", students=names)` does this:
1. Opens `templates/home.html`
2. Replaces `{{ title }}` with `"Our Class"`
3. Replaces `{{ students }}` with the list of names
4. Runs the `{% for %}` loop to generate `<li>` for each student
5. Returns the final HTML to the browser

### Template Syntax

```
{{ variable }}                         — print a value
{% for item in list %}...{% endfor %}  — loop
{% if condition %}...{% endif %}        — condition
{% if x %}...{% else %}...{% endif %}   — if/else
{{ loop.index }}                        — current iteration number (1, 2, 3...)
```

These `{{ }}` and `{% %}` tags only work inside template files, not in regular Python.

---

## What is JSON? Returning JSON (for APIs)

**JSON** (JavaScript Object Notation) is a text format for sending data. It looks almost identical to Python dictionaries:

```json
{"name": "Timur", "score": 89, "group": 1}
```

When you're building an **API** (a service that sends data, not web pages), you return JSON instead of HTML. Mobile apps, frontend JavaScript, and other services consume JSON.

```python
from flask import Flask, jsonify

app = Flask(__name__)

students_data = {
    "Timur": {"score": 89, "group": 1},
    "Shahrom": {"score": 83, "group": 1},
    "Nizar": {"score": 72, "group": 1},
}


@app.route("/api/students")
def all_students():
    return jsonify(students_data)


@app.route("/api/student/<n>")
def one_student(name):
    if name in students_data:
        return jsonify(students_data[name])
    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
```

`jsonify()` converts a Python dictionary into a JSON response. The `404` is an HTTP status code meaning "not found."

```
localhost:5000/api/students           -> full JSON with all students
localhost:5000/api/student/Timur      -> {"score": 89, "group": 1}
localhost:5000/api/student/Unknown    -> {"error": "Student not found"}
```

---

## What are HTTP Methods? Handling Forms (POST)

When your browser communicates with a server, it uses **HTTP methods**:

```
GET  — "give me data"        (visiting a page, clicking a link)
POST — "here's some data"    (submitting a form, sending information)
```

By default, Flask routes only respond to GET. To handle form submissions, you need to allow POST:

`templates/login.html`:

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Login</h1>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Your name">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
</body>
</html>
```

`app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if password == "python123":
            message = f"Welcome, {username}!"
        else:
            message = "Wrong password"
    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
```

How this works:
1. User visits `/login` (GET) — sees the empty form
2. User fills in the form and clicks Submit — browser sends a POST request
3. Flask receives the POST, reads `request.form["username"]` and `request.form["password"]`
4. Python checks the password and creates a message
5. The template shows the message

`methods=["GET", "POST"]` tells Flask this route accepts both types of requests.

`request.form["field_name"]` reads the value from the submitted form. The `name` attribute in HTML (`name="username"`) must match the key you use in Python (`request.form["username"]`).

---

## Full Mini-Project — Student Scoreboard

This combines everything: routes, templates, forms, JSON API.

`app.py`:

```python
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

students = []


@app.route("/")
def home():
    ranked = sorted(students, key=lambda s: s["score"], reverse=True)
    return render_template("scoreboard.html", students=ranked)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        score = int(request.form["score"])
        students.append({"name": name, "score": score})
        return redirect("/")
    return render_template("add.html")


@app.route("/api/students")
def api_students():
    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True)
```

`redirect("/")` sends the user back to the home page after adding a student. Without it, the user would stay on the `/add` page.

`templates/scoreboard.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Scoreboard</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background: #333; color: white; }
        a { display: inline-block; margin: 20px 0; color: #333; }
    </style>
</head>
<body>
    <h1>Scoreboard</h1>
    <a href="/add">+ Add Student</a>

    {% if students %}
    <table>
        <tr><th>#</th><th>Name</th><th>Score</th></tr>
        {% for s in students %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.score }}%</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
        <p>No students yet.</p>
    {% endif %}
</body>
</html>
```

`templates/add.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Student</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 40px auto; }
        input, button { display: block; width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { background: #333; color: white; border: none; cursor: pointer; }
        a { color: #333; }
    </style>
</head>
<body>
    <h1>Add Student</h1>
    <form method="POST">
        <input type="text" name="name" placeholder="Student name" required>
        <input type="number" name="score" placeholder="Score (0-100)" min="0" max="100" required>
        <button type="submit">Add</button>
    </form>
    <a href="/">Back to scoreboard</a>
</body>
</html>
```

---

## uv Commands Reference

```bash
uv init                  # create a new project
uv add flask             # install a library
uv add flask jinja2      # install multiple libraries at once
uv remove flask          # uninstall a library
uv run app.py            # run a file with all project dependencies available
uv run flask run         # alternative way to start a Flask server
```

---

## Project Structure

```
my_flask_app/
    app.py               # main application — your Python code
    pyproject.toml        # dependencies — managed by uv automatically
    templates/            # HTML template files
        home.html
        login.html
    static/               # static files — CSS, JavaScript, images
        style.css
        script.js
```

Flask automatically looks for templates in `templates/` and static files in `static/`. These folder names are required by convention.

---

## Quick Reference

| Concept | Code |
|---------|------|
| Create project | `uv init` |
| Install library | `uv add flask` |
| Run app | `uv run app.py` |
| Create route | `@app.route("/path")` |
| Dynamic URL | `@app.route("/user/<n>")` |
| Return HTML template | `return render_template("file.html", data=data)` |
| Return JSON | `return jsonify(data)` |
| Get form data | `request.form["field"]` |
| Redirect to another page | `return redirect("/")` |
| Allow POST requests | `@app.route("/path", methods=["GET", "POST"])` |
| Debug mode | `app.run(debug=True)` |

---

## Summary — How It All Connects

```
1. uv init              — create the project
2. uv add flask         — install Flask
3. app = Flask(__name__) — create the app object
4. @app.route("/")      — decorator registers a URL
5. def home():          — function handles that URL
6. return ...           — send response (text, HTML, JSON)
7. app.run()            — start the server
8. uv run app.py        — run everything
```

```
Browser                          Flask App
   |                                |
   |--- GET /student/Timur -------->|
   |                                | finds @app.route("/student/<name>")
   |                                | calls student(name="Timur")
   |                                | function returns "Hello, Timur!"
   |<------ "Hello, Timur!" --------|
   |                                |
```
