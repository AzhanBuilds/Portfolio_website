from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

    if Project.query.count() == 0:
        db.session.add(Project(
            title="Portfolio Website",
            description="Modern portfolio built with Flask.",
            image="project12.jpg",
            link = "#"
        ))

        db.session.add(Project(
            title="Personal Blog",
            description="Blog application using Flask.",
            image="project2.jpg",
            link="#"
        ))

        db.session.commit()

# Home Route
@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Projects Route
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Skill Route
@app.route("/skills")
def skills():
    return render_template("skills.html")

# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        if not name or not email or not message:
            flash('All fields are required!', 'error')
        else:
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('home'))
    
    return render_template('contact.html')

# Error Route
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )







