# Flask Calculator — Assignments
## Extending the Scientific Calculator

> These assignments build directly on the project from Lesson 2.  
> Do not start a new project. Extend what you already have.  
> All Python code must be written by yourself. AI may only be used for HTML and CSS.

---

## Assignment 1 — Unit Converter

**Difficulty: Medium**

Add a new page `/converter` that converts between common units using OOP.

### Requirements

1. Create a new class `UnitConverter` in a file `converter.py`
2. It must support at least the following conversion categories:

| Category | Units |
|---|---|
| Length | meters, kilometers, miles, feet, inches |
| Temperature | Celsius, Fahrenheit, Kelvin |
| Weight | kilograms, grams, pounds, ounces |

3. Add a new route `/converter` in `app.py` with GET and POST methods
4. The form lets the user choose a category, enter a value, and select input/output units
5. The result must be displayed on the same page
6. All conversion errors (invalid input, same unit, unsupported combination) must be handled with clear messages

### Class structure to follow

```python
class UnitConverter:
    def convert(self, category, value, from_unit, to_unit):
        """
        Perform the conversion.
        Raises ValueError for unsupported units or categories.
        """
        pass

    def get_units(self, category):
        """
        Return a list of available units for a given category.
        Used to populate the dropdown in the template.
        """
        pass
```

### Grading note

Hardcoding `if from_unit == 'km' and to_unit == 'miles'` for every possible pair is not acceptable.  
Use a base unit approach — convert everything to a base unit first, then to the target unit.

---

## Assignment 2 — Calculation Statistics

**Difficulty: Medium**

Extend `HistoryManager` to provide statistics about past calculations.

### Requirements

1. Add the following methods to the `HistoryManager` class:

```python
def get_stats(self):
    """
    Read history.txt and return a dictionary with:
    - total_calculations: int
    - most_used_operation: str
    - average_result: float (average of all numeric results)
    - largest_result: float
    - smallest_result: float
    """
    pass
```

2. Add a new route `/stats` that calls `history.get_stats()` and renders a `stats.html` template
3. Display all statistics clearly on the page
4. If history is empty, show a message instead of crashing
5. Handle cases where a result may be non-numeric (e.g. error entries should be skipped)

### Expected output example

```
Total calculations:   47
Most used operation:  +
Average result:       318.44
Largest result:       99856.0
Smallest result:      -42.0
```

---

## Assignment 3 — User Sessions

**Difficulty: Medium-Hard**

Right now every user shares the same `history.txt`. Add session support so each browser session has its own history.

### Requirements

1. Use Flask's built-in `session` object (you will need to set a `SECRET_KEY`)
2. Each session must have a unique ID — use Python's `uuid` module
3. Save history to a file named after the session ID: `history_<session_id>.txt`
4. Modify `HistoryManager.__init__` to accept a session ID and build the filepath from it
5. The `/history` page must only show the current user's calculations
6. Add a route `/clear-session` that clears the session and deletes the session history file

### Hint

```python
import uuid
from flask import session

# In app.py before_request:
if 'session_id' not in session:
    session['session_id'] = str(uuid.uuid4())
```

### What not to use

Do not use any database. Files only.

---

## Assignment 4 — REST API Endpoint

**Difficulty: Hard**

Add a JSON API to your calculator so it can be used programmatically, not just through the browser.

### Requirements

1. Create a new route `POST /api/calculate` that accepts JSON input and returns JSON output
2. The request body format:

```json
{
  "operation": "sqrt",
  "num1": 144,
  "num2": null
}
```

3. On success, return:

```json
{
  "success": true,
  "expression": "sqrt(144)",
  "result": 12.0
}
```

4. On error, return with the appropriate HTTP status code:

```json
{
  "success": false,
  "error": "Square root of a negative number is not defined."
}
```

5. Reuse the existing `Calculator` class — do not duplicate any math logic
6. Save successful API calculations to history as well (mark them with `[API]` prefix)
7. Handle missing or malformed JSON with a `400 Bad Request` response

### Testing your API

You must test your endpoint using one of the following tools and include screenshots in your submission:

- `curl` from the terminal
- Postman
- A simple Python script using the `requests` library

### Hint

```python
from flask import jsonify

request.get_json()        # parse incoming JSON body
jsonify({...})            # return a JSON response
return jsonify({...}), 400  # return with a custom status code
```

---

## Assignment 5 — Calculation Graph

**Difficulty: Hard**

Visualize the history of calculations as a chart on the `/stats` page.

### Requirements

1. Read all numeric results from `history.txt`
2. Plot them as a **line chart** showing result values over time (by calculation index)
3. The chart must be generated server-side using `matplotlib` and sent to the browser as an image — no JavaScript charting libraries allowed
4. Display the chart on the `/stats` page above the statistics table

### How to send a chart as an image from Flask

```python
import matplotlib
matplotlib.use('Agg')  # use non-interactive backend
import matplotlib.pyplot as plt
import io
from flask import send_file

def generate_chart(values):
    fig, ax = plt.subplots()
    ax.plot(values)
    ax.set_title('Calculation Results Over Time')
    ax.set_xlabel('Calculation #')
    ax.set_ylabel('Result')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf
```

5. Add a new route `/stats/chart` that returns the image, then embed it in `stats.html`:

```html
<img src="/stats/chart" alt="Calculation chart">
```

### Install matplotlib

```bash
pip install matplotlib
```

---

## Submission Requirements

For each assignment you complete, your submission must include:

1. All modified and new `.py` files
2. All new templates (`.html` files)
3. A short `README.md` (5–10 lines) explaining what you built and how to run it
4. For Assignment 4: screenshots of your API tests

Submit as a `.zip` file named `firstname_lastname_assignment_N.zip`

---

## Grading Criteria

| Criterion | Weight |
|---|---|
| Code runs without errors | 30% |
| OOP structure is correct (classes, methods, separation of concerns) | 30% |
| Error handling covers all edge cases | 20% |
| Code is readable and consistently formatted | 20% |

Late submissions will lose 10% per day.
