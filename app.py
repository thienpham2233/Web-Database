from flask import Flask, render_template, request, flash, redirect, url_for
from Model import DatabaseModel

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create an instance of DatabaseModel globally so that it's shared across routes
db_model = None

@app.route("/", methods=["GET", "POST"])
def index():
    global db_model
    if request.method == "POST":
        # Connect to the database
        db_name = request.form.get("db_name")
        user = request.form.get("user")
        password = request.form.get("password")
        host = request.form.get("host")
        port = request.form.get("port")

        try:
            db_model = DatabaseModel(db_name, user, password, host, port)
            flash("Connected to the database successfully!", "success")
        except Exception as e:
            flash(f"Error connecting to the database: {e}", "danger")
            db_model = None

    return render_template("index.html", db_model=db_model)

@app.route("/load_data", methods=["POST"])
def load_data():
    if db_model:
        table_name = request.form.get("table_name")
        rows = db_model.load_data(table_name)
        return render_template("index.html", rows=rows)
    else:
        flash("No database connection", "danger")
        return redirect(url_for('index'))

@app.route("/insert_data", methods=["POST"])
def insert_data():
    if db_model:
        table_name = request.form.get("table_name")
        column1 = request.form.get("column1")
        column2 = request.form.get("column2")
        column3 = request.form.get("column3")
        try:
            db_model.insert_data(table_name, column1, column2, column3)
            flash("Data inserted successfully!", "success")
        except Exception as e:
            flash(f"Error inserting data: {e}", "danger")
    else:
        flash("No database connection", "danger")
    return redirect(url_for('index'))

@app.route("/delete_data", methods=["POST"])
def delete_data():
    if db_model:
        selected_rows = request.form.getlist("selected_rows")
        db_model.delete_data(selected_rows)
        flash("Selected data deleted successfully!", "success")
    else:
        flash("No database connection", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
