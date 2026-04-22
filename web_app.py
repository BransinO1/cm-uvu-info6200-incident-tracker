# web_app.py
# INFO 6200 - Module 13 Assignment
# Created by: Corbin Meacham

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask import jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
uri = os.getenv("DATABASE_URL", "sqlite:///project.db")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Model
class Incident(db.Model):
    incident_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    reported_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"<Incident {self.title}>"

# Create DB
def init_db():
    with app.app_context():
        db.create_all()

init_db()

# HOME ROUTE
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    incidents = Incident.query.filter_by(user_id=session["user_id"]).all()

    return render_template("incidents.html", incidents=incidents, user=user)

@app.route("/api/v1/incidents", methods=["GET"])
def api_get_incidents():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    incidents = Incident.query.filter_by(user_id=session["user_id"]).all()

    data = []
    for incident in incidents:
        data.append({
            "id": incident.incident_id,
            "title": incident.title,
            "description": incident.description,
            "date": incident.incident_date,
            "status": incident.status,
            "reported_by": incident.reported_by,
            "created_at": incident.created_at,
            "updated_at": incident.updated_at
        })

    return jsonify(data)

@app.route("/api/v1/incidents/<int:incident_id>", methods=["GET"])
def api_get_incident(incident_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    incident = Incident.query.get(incident_id)

    if not incident:
        return jsonify({"error": "Not found"}), 404

    # Ownership check
    if incident.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = {
        "id": incident.incident_id,
        "title": incident.title,
        "description": incident.description,
        "date": incident.incident_date,
        "status": incident.status,
        "reported_by": incident.reported_by,
        "created_at": incident.created_at,
        "updated_at": incident.updated_at
    }

    return jsonify(data)

# USER REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        # Render error page with a link back to registration
        return render_template(
            "message.html",
            title="Registration Error",
            message="Username already exists",
            back_link=url_for("register")
        )

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))

# USER LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.user_id
        return redirect(url_for("home"))

    # Render error page with a link back to login
    return render_template(
        "message.html",
        title="Login Error",
        message="Invalid username or password",
        back_link=url_for("login")
    )

# USER LOGOUT
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# CREATE
@app.route("/add", methods=["GET", "POST"])
def add_incident():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("add.html")

    new_incident = Incident(
        title=request.form.get("title"),
        description=request.form.get("description"),
        incident_date=request.form.get("incident_date"),
        reported_by=request.form.get("reported_by"),
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_id=session["user_id"]
    )

    db.session.add(new_incident)
    db.session.commit()

    return redirect(url_for("home"))

# UPDATE
@app.route("/edit/<int:incident_id>", methods=["GET", "POST"])
def edit_incident(incident_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    incident = Incident.query.get_or_404(incident_id)

    if incident.user_id != session["user_id"]:
        return "Unauthorized"

    if request.method == "POST":
        incident.title = request.form.get("title")
        incident.description = request.form.get("description")
        incident.incident_date = request.form.get("incident_date")
        incident.reported_by = request.form.get("reported_by")
        incident.status = request.form.get("status")

        incident.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", incident=incident)

# DELETE
@app.route("/delete/<int:incident_id>")
def delete_incident(incident_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    incident = Incident.query.get_or_404(incident_id)

    if incident.user_id != session["user_id"]:
        return "Unauthorized"

    db.session.delete(incident)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)