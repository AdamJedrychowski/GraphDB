from database import GraphDB
from flask import Flask, render_template, redirect, request
import sys

app = Flask(__name__)
db = GraphDB('neo4j+s://5f35737e.databases.neo4j.io', 'neo4j', 'PASSWORD')

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/movie')
def all_movies():
    return render_template('all_movies.html', movies=db.get_all_movies())


@app.route('/employees')
def all_employees():
    return render_template('all_employees.html', employees=db.get_all_employees())


@app.route('/movie/add', methods=('GET', 'POST'))
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        premiere = request.form['premiere']
        rating = request.form['rating']
        try:
            float(rating)
            if title.strip() and premiere.strip():
                db.add_movie(title, premiere, rating)
        except ValueError:
            pass
        return redirect('/')
    
    return render_template('add_movie.html')


@app.route('/employee/add', methods=('GET', 'POST'))
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        if name.strip() and surname.strip() and age.isnumeric():
            db.add_person(name, surname, age)
        return redirect('/')

    return render_template('add_employee.html')


@app.route('/employee/assign/<id>', methods=('GET', 'POST'))
def assign_employee(id):
    if request.method == 'POST':
        role = request.form.get('role')
        movie_id = request.form.get('movie')
        if role and movie_id:
            db.assign_employee(id, movie_id, role)
        return redirect('/')

    roles = ['Produced', 'Directed', 'RecordedSound', 'Acted', 'Wrote']
    return render_template('assign_employee.html', roles=roles, movies=db.get_all_movies())


@app.route('/movie/employees/<id>')
def movie_crew(id):
    return render_template("movie_crew.html", crew=db.get_movie_crew(id))


@app.route('/movie/options/<id>')
def movie_options(id):
    return render_template("movie_options.html", id=id)


@app.route('/employee/options/<id>')
def employee_actions(id):
    return render_template("employee_options.html", id=id)


@app.route('/employee/movies/<id>')
def employee_movies(id):
    return render_template('employee_movies.html', movies=db.get_employee_movies(id))


@app.route('/employee/remove/<id>', methods=('GET', 'POST'))
def employee_remove(id):
    db.remove_employee(id)
    return redirect('/')


@app.route('/employee/update/<id>', methods=('GET', 'POST'))
def employee_update(id):
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        if name.strip() and surname.strip() and age.isnumeric():
            db.update_person(id, name, surname, age)
        return redirect('/')

    return render_template('update_employee.html', empl=db.get_employee(id))


@app.route('/movie/remove/<id>', methods=('GET', 'POST'))
def movie_remove(id):
    db.remove_movie(id)
    return redirect('/')


@app.route('/movie/update/<id>', methods=('GET', 'POST'))
def movie_update(id):
    if request.method == 'POST':
        title = request.form['title']
        premiere = request.form['premiere']
        rating = request.form['rating']
        try:
            float(rating)
            if title.strip() and premiere.strip():
                db.update_movie(id, title, premiere, rating)
        except ValueError:
            pass
        return redirect('/')

    return render_template('update_movie.html', movie=db.get_movie(id))


@app.route('/filter', methods=('GET', 'POST'))
def filter():
    if request.method == 'POST':
        role = request.form['role']
        rating = request.form['rating']
        age = request.form['age']
        name = request.form['name']
        surname = request.form['surname']
        title = request.form['title']
        premiere = request.form['premiere']
        top = request.form['top']
        sort = request.form['sort']
        return render_template("filter.html", objects=db.filter_db(role, rating, age, name, surname, title, premiere, top, sort))
        
    return render_template("filter.html")
