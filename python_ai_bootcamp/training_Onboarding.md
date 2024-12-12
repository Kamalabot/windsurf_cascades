# Training and Onboarding Application

This project is a simple web application built with Flask that allows users to view training materials and track their progress. Below are the details and code for each part of the application.

## Project Structure

training_onboarding_app/ 
│
├── app.py 
├── templates/ 
│ ├── index.html 
│ ├── training.html 
│ └── progress.html 
└── static/ 
└── style.css


## 1. `app.py`
This is the main application file that sets up the Flask app and routes.

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample training materials
training_materials = [
    {"id": 1, "title": "Introduction to Python", "completed": False},
    {"id": 2, "title": "Data Analysis with Pandas", "completed": False},
    {"id": 3, "title": "Machine Learning Basics", "completed": False},
]

@app.route('/')
def index():
    return render_template('index.html', materials=training_materials)

@app.route('/training/<int:training_id>', methods=['GET', 'POST'])
def training(training_id):
    if request.method == 'POST':
        # Mark the training as completed
        training_materials[training_id - 1]['completed'] = True
        return redirect(url_for('index'))
    return render_template('training.html', training=training_materials[training_id - 1])

@app.route('/progress')
def progress():
    completed_materials = [m for m in training_materials if m['completed']]
    return render_template('progress.html', completed=completed_materials)

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. `templates/index.html`

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Training Dashboard</title>
</head>
<body>
    <h1>Training Materials</h1>
    <ul>
        {% for material in materials %}
            <li>
                <a href="{{ url_for('training', training_id=material.id) }}">{{ material.title }}</a>
                {% if material.completed %} - Completed {% endif %}
            </li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('progress') }}">View Progress</a>
</body>
</html>
```

## 3. `templates/training.html`

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>{{ training.title }}</title>
</head>
<body>
    <h1>{{ training.title }}</h1>
    <p>Content for {{ training.title }} goes here.</p>
    <form method="POST">
        <button type="submit">Mark as Completed</button>
    </form>
    <a href="{{ url_for('index') }}">Back to Dashboard</a>
</body>
</html>
```

## 4. `templates/progress.html`

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Your Progress</title>
</head>
<body>
    <h1>Your Completed Trainings</h1>
    <ul>
        {% for material in completed %}
            <li>{{ material.title }}</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('index') }}">Back to Dashboard</a>
</body>
</html>
```

## 5. `static/style.css`

body {
    font-family: Arial, sans-serif;
    margin: 20px;
}

h1 {
    color: #333;
}

ul {
    list-style-type: none;
}

a {
    text-decoration: none;
    color: blue;
}
```

```
pip install Flask
python app.py
```
