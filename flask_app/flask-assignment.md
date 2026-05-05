# Assignment: Flask Web Application

---

## Setup

```bash
mkdir flask_app
cd flask_app
uv init
uv add flask
```

All your code goes in this folder. Create `app.py` as your main file.

---

## Task 1 — Home Page (10 pts)

Create a Flask app with a route `/` that returns an HTML page with:

- Your name as a heading
- A short paragraph about yourself
- Links to `/students` and `/about`

```
localhost:5000/
```

---

## Task 2 — About Page (10 pts)

Create a route `/about` that returns an HTML page with:

- A heading "About This App"
- A paragraph explaining what this app does
- A link back to `/`

```
localhost:5000/about
```

---

## Task 3 — Students List (15 pts)

Create a route `/students` that displays all students from the class as an HTML page.

Use the following data inside your `app.py`:

```python
students_data = {
    "Abdul-Aziz": 77, "Abdullo": 47, "Abubakr": 59,
    "Ahmadjon": 69, "Amir": 44, "Behruz": 69,
    "Habibulloh": 51, "Ilyos": 64, "Maftunbek": 39,
    "Maryam": 28, "Mubarro": 22, "Najmiya": 60,
    "Otabek": 48, "Shahrom": 83, "Habibullo": 63,
    "Rukhshona": 31, "Osiya": 69, "Bakhtiyor": 32,
    "Muhammadjon": 0, "Timur": 89, "Gulsum": 36,
    "Rayhona": 39, "Abduvozit": 12, "Ismoiljon": 0,
    "Nizar": 72,
}
```

Requirements:
- Use a **template** (`templates/students.html`)
- Display students in an HTML table with columns: #, Name, Score
- Students must be **sorted by score** (highest first)

```
localhost:5000/students
```

---

## Task 4 — Individual Student Page (15 pts)

Create a route `/student/<name>` that shows information about a single student.

- If the student exists, show their name and score
- If the student does not exist, show "Student not found" and return status code 404
- Show a message based on score:
  - 80+ : "Excellent"
  - 50-79 : "Good"
  - 1-49 : "Needs improvement"
  - 0 : "No data"
- Use a **template**

```
localhost:5000/student/Timur      -> shows Timur's info
localhost:5000/student/Unknown    -> shows "Student not found"
```

---

## Task 5 — JSON API (15 pts)

Create two API routes that return JSON:

`/api/students` — returns all students as JSON

```json
{"Abdul-Aziz": 77, "Abdullo": 47, ...}
```

`/api/student/<name>` — returns one student as JSON

```json
{"name": "Timur", "score": 89, "status": "Excellent"}
```

If student not found:

```json
{"error": "Student not found"}
```

with status code 404.

```
localhost:5000/api/students
localhost:5000/api/student/Shahrom
localhost:5000/api/student/Nobody
```

---

## Task 6 — Add Student Form (20 pts)

Create a page `/add` with an HTML form where a user can add a new student.

The form should have:
- A text input for the student's name
- A number input for the score (0-100)
- A submit button

When the form is submitted:
- Validate that the name is not empty
- Validate that the score is between 0 and 100
- If a student with that name already exists, show an error message
- If everything is valid, add the student to `students_data` and redirect to `/students`

Requirements:
- The route must accept both GET and POST methods
- Use a **template** for the form
- Show error messages inside the template if validation fails

```
localhost:5000/add
```

---

## Task 7 — Styling (15 pts)

Make your app look presentable. Create a `static/style.css` file and link it in your templates.

Requirements:
- All pages use the same CSS file
- Table has borders and padding
- Links are styled (no default blue underline)
- Pages have a consistent layout (centered content, readable font)
- Form inputs and buttons are styled

To link CSS in a template:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

---

## Bonus — Search (10 pts)

Add a search feature to the `/students` page.

- Add a text input at the top of the page
- When the user types a name and submits, filter the table to show only matching students
- Partial matches should work (typing "ah" should show "Ahmadjon", "Shahrom", etc.)
- If no matches found, show "No students found"

Hint: use a GET form with a query parameter.

```python
search = request.args.get("search", "")
```

```
localhost:5000/students?search=ah
```

---

## Project Structure

```
flask_app/
    app.py
    pyproject.toml
    templates/
        home.html
        about.html
        students.html
        student.html
        add.html
    static/
        style.css
```

---

## Requirements

- All HTML must be in template files, not inside Python strings
- All routes must work without errors
- Code must be clean and readable
- Use `uv run app.py` to run

---

## Grading

| Task | Points |
|------|--------|
| Task 1 — Home Page | 10 |
| Task 2 — About Page | 10 |
| Task 3 — Students List | 15 |
| Task 4 — Individual Student Page | 15 |
| Task 5 — JSON API | 15 |
| Task 6 — Add Student Form | 20 |
| Task 7 — Styling | 15 |
| Bonus — Search | +10 |
| **Total** | **100 (+10)** |

---

## Submission

Push your code to your git repository. Make sure the project runs with:

```bash
cd flask_app
uv run app.py
```
