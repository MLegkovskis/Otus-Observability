
from functools import wraps
from time import time

# Dictionary to store telemetry data
telemetry_data = {
    "/": {"GET": {"count": 0, "response_time": 0}},
    "/add": {"POST": {"count": 0, "response_time": 0}},
    "/update": {"POST": {"count": 0, "response_time": 0}}
}

def telemetry_decorator(endpoint=None, method=None):
    def decorator(f):
        """
        A decorator to gather telemetry data (response time, response code) for the given endpoint and method.
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time()
            response = f(*args, **kwargs)
            end_time = time()

            telemetry_data[endpoint][method]["count"] += 1
            telemetry_data[endpoint][method]["response_time"] += (end_time - start_time)

            return response

        return wrapper

    return decorator


from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route("/")
@telemetry_decorator(endpoint="/", method="GET")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route('/add', methods=["POST"])
@telemetry_decorator(endpoint="/add", method="POST")
def add():
    data = request.form["todo_item"]
    todo = Todo(text=data, complete=False)
    db.session.add(todo)
    db.session.commit()
    # return data # DEBUG REQUEST
    return redirect(url_for("index"))


@app.route('/update', methods=["POST"])
@telemetry_decorator(endpoint="update", method="POST")

def update():
    # return request.form # DEBUG REQUEST
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/metrics')
def metrics():
    output = []
    
    # Convert telemetry_data to Prometheus format
    for endpoint, methods_data in telemetry_data.items():
        for method, data in methods_data.items():
            metric_name = f"{endpoint.replace('/', '')}_{method.lower()}_requests_total"
            output.append(f"# HELP {metric_name} The total number of {method} requests to {endpoint}.")
            output.append(f"# TYPE {metric_name} counter")
            output.append(f"{metric_name} {data['count']}")
            
            metric_name_response_time = f"{endpoint.replace('/', '')}_{method.lower()}_response_time_total_seconds"
            output.append(f"# HELP {metric_name_response_time} The total response time (in seconds) for {method} requests to {endpoint}.")
            output.append(f"# TYPE {metric_name_response_time} counter")
            output.append(f"{metric_name_response_time} {data['response_time']:.6f}")
    
    return '\\n'.join(output) + '\\n'  # Ensure each metric is on a new line
