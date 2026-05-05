#  Flask 
## OOP · Scientific Calculator · Error Handling · File I/O

> **Prerequisites:** Flask is installed. You are familiar with routes, templates, and lists from pervious lesson (quick_start.md).

---

## What You Will Learn 

| Topic | Description |
|---|---|
| OOP in Flask | Separate your logic into classes instead of writing everything in one function |
| Scientific Calculator | Support operations like square root, sin, cos, log and more |
| Error Handling | Catch bad input, math errors, and HTTP errors gracefully |
| File I/O | Write calculation history to a file and read it back through the browser |

---

## Important Rule

You are allowed to use AI tools (ChatGPT, Claude, etc.) to help with **HTML and CSS only**.  
All **Python code must be written by yourself.** If you cannot explain what a line of code does, you should not submit it.

---

## Part 1 — Project Structure

```
flask_calculator/
│
├── app.py
├── calculator.py
├── history_manager.py
├── history.txt
└── templates/
    ├── index.html
    └── history.html
```

The idea is simple: `app.py` handles only routing. All math logic goes into `calculator.py`, and all file operations go into `history_manager.py`. This is the foundation of clean OOP design.

---

## Part 2 — OOP Design

### Why use classes here?

In Lesson 1 you wrote everything inside route functions. That works for small scripts, but as the project grows it becomes hard to maintain. By separating concerns into classes:

- You can test each class independently
- Your `app.py` stays clean and readable
- Each class has a single responsibility

---

### `calculator.py` — class skeleton

```python
import math

class Calculator:
    """Handles all mathematical operations."""

    SUPPORTED_OPERATIONS = ['+', '-', '*', '/', 'sqrt', 'pow', 'sin', 'cos', 'tan', 'log', 'log10']

    def calculate(self, operation, num1, num2=None):
        """
        Perform a calculation.
        num2 is optional — not needed for operations like sqrt, sin, cos, etc.
        Returns the numeric result.
        Raises ValueError or ZeroDivisionError on invalid input.
        """
        # TODO: Task 1 — implement this method
        pass

    def format_expression(self, operation, num1, num2=None):
        """
        Return a human-readable string of the expression.
        Example: "sqrt(25)", "10 + 5", "sin(90)"
        """
        # TODO: Task 1 — implement this method
        pass
```

---

### `history_manager.py` — class skeleton

```python
class HistoryManager:
    """Handles reading and writing calculation history to a file."""

    def __init__(self, filepath='history.txt'):
        self.filepath = filepath

    def save(self, expression, result):
        """Append one entry to the history file."""
        # TODO: Task 3 — implement this method
        pass

    def load(self):
        """Read all lines from the history file. Return empty list if file not found."""
        # TODO: Task 4 — implement this method
        pass

    def clear(self):
        """Erase all content from the history file."""
        # TODO: Bonus — implement this method
        pass
```

---

### `app.py` — starter code

```python
from flask import Flask, render_template, request, redirect, url_for
from calculator import Calculator
from history_manager import HistoryManager

app = Flask(__name__)
calc = Calculator()
history = HistoryManager()


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = None
    error = None

    if request.method == 'POST':
        pass  # TODO: Task 2 — handle form submission

    return render_template('index.html',
                           result=result,
                           expression=expression,
                           error=error,
                           operations=Calculator.SUPPORTED_OPERATIONS)


@app.route('/history')
def history_page():
    entries = history.load()
    return render_template('history.html', entries=entries)


@app.route('/clear-history', methods=['POST'])
def clear_history():
    # TODO: Bonus
    pass


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
```

---

## Part 3 — Supported Operations

Your calculator must support the following:

| Operation | Input type | Example |
|---|---|---|
| `+` `-` `*` `/` | two numbers | `10 / 4` |
| `pow` | two numbers (base, exponent) | `2 ^ 8` |
| `sqrt` | one number | `sqrt(144)` |
| `sin` `cos` `tan` | one number (degrees) | `sin(90)` |
| `log` | one number (natural log) | `ln(e)` |
| `log10` | one number | `log10(1000)` |

> Note: Python's `math` module works in **radians**. You must convert degrees to radians using `math.radians()` before passing to `math.sin()`, `math.cos()`, `math.tan()`.

---

## Part 4 — Error Handling

### Logic errors — wrap all calculations in try/except

```python
try:
    result = calc.calculate(operation, num1, num2)
except ZeroDivisionError:
    error = "Division by zero is not allowed."
except ValueError as e:
    error = str(e)
except Exception as e:
    error = "An unexpected error occurred."
```

### Errors your Calculator class must raise explicitly

- `ValueError("num2 is required for this operation")` — when a two-number operation receives only one
- `ValueError("Square root of a negative number is not defined")` — `sqrt` of negative
- `ValueError("Logarithm requires a positive number")` — `log` of zero or negative
- `ZeroDivisionError` — division by zero
- `ValueError("Unsupported operation")` — unknown operation string

---

## Tasks

Complete tasks in order. Do not skip ahead.

---

### Task 1 — Implement the Calculator class

Inside `calculator.py`:

1. Implement `calculate(operation, num1, num2=None)` to handle all operations listed in Part 3
2. Implement `format_expression(operation, num1, num2=None)` to return a readable string
3. Raise appropriate exceptions as described in Part 4

Do not write any Flask code in this file. Test your class directly in the terminal first:

```python
c = Calculator()
print(c.calculate('sqrt', 144))       # 12.0
print(c.calculate('+', 10, 5))        # 15.0
print(c.calculate('sin', 90))         # 1.0
print(c.format_expression('pow', 2, 8))  # "2 ^ 8"
```

---

### Task 2 — Connect the form to the Calculator

Inside the `POST` block in `app.py`:

1. Read `operation`, `num1`, and optionally `num2` from `request.form`
2. Convert inputs to `float` where needed
3. Call `calc.calculate()` and `calc.format_expression()`
4. Wrap everything in `try/except` and store errors in the `error` variable
5. Pass `result`, `expression`, and `error` to the template

The template already has placeholders for these variables.

---

### Task 3 — Implement HistoryManager.save()

1. Each successful calculation should be saved to `history.txt`
2. Format: `expression = result` on a new line
3. If the file does not exist, Python will create it automatically when opened in append mode

Call `history.save()` from `app.py` only after a successful calculation (not on errors).

---

### Task 4 — Implement HistoryManager.load() and display history

1. Implement `load()` to return a list of lines from `history.txt`
2. Handle `FileNotFoundError` — return an empty list if the file does not exist
3. The `/history` route already passes `entries` to the template
4. In `history.html`, display each entry in a list
5. If `entries` is empty, show the message: `"No calculations have been recorded yet."`

---

### Task 5 — Custom error pages

1. Create `templates/404.html` with a message and a link back to `/`
2. Create `templates/500.html` with a message explaining something went wrong
3. Both handlers are already registered in `app.py` — you only need the templates

Test the 404 page by visiting any non-existent URL such as `/xyz`.

---

### Bonus — Clear History

1. Implement `HistoryManager.clear()` to erase all content in `history.txt`
2. Connect it to the `/clear-history` route in `app.py`
3. After clearing, redirect back to `/history`
4. Add a "Clear History" button to `history.html` that submits a POST form to `/clear-history`

---

## Checklist

Before submitting, verify each point:

- [ ] `Calculator` class is in its own file with no Flask imports
- [ ] `HistoryManager` class is in its own file with no Flask imports
- [ ] All four basic operations work correctly
- [ ] All scientific operations work correctly (sqrt, sin, cos, tan, log, log10, pow)
- [ ] Division by zero returns an error message, not a crash
- [ ] Invalid input (letters in number fields) is handled
- [ ] Every successful result is written to `history.txt`
- [ ] `/history` displays all saved entries
- [ ] Custom 404 page is working
- [ ] Bonus: clear history button works

---

## Reference

```python
import math

math.sqrt(x)        # square root
math.pow(x, y)      # x to the power of y
math.sin(x)         # x must be in radians
math.cos(x)
math.tan(x)
math.radians(deg)   # convert degrees to radians
math.log(x)         # natural logarithm
math.log10(x)       # base-10 logarithm
```

```python
# Flask quick reference
request.form['field']          # read form field (raises error if missing)
request.form.get('field')      # read form field (returns None if missing)
redirect(url_for('index'))     # redirect to a route by function name
```

---

Deadline and submission instructions will be announced separately.
