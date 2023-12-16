from neo4j import GraphDatabase
from neo4j.time import Date
from neo4j.exceptions import AuthError

class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        try:
            self.driver.verify_connectivity()
        except Exception as e:
            print(e.message)

    def add_person(self, name, surname, age):
        query = 'CREATE (e:Employee {name:$name, surname:$surname, age:$age}) RETURN elementId(e);'
        with self.driver.session() as session:
            return session.run(query, name=name, surname=surname, age=int(age)).value()[0]

    def add_movie(self, title, premiere, rating):
        query = 'CREATE (m:Movie {title:$title, premiere:$premiere, rating:$rating}) RETURN elementId(m);'
        with self.driver.session() as session:
            return session.run(query, title=title, premiere=Date.parse(premiere), rating=float(rating)).value()[0]

    def get_all_employees(self):
        query = 'MATCH (e:Employee) RETURN e'
        with self.driver.session() as session:
            return(session.run(query).value())

    def get_all_movies(self):
        query = 'MATCH (m:Movie) RETURN m'
        with self.driver.session() as session:
            return session.run(query).value()

    def assign_employee(self, empl_id, movie_id, role):
        query = 'MATCH (e:Employee), (m:Movie) WHERE elementId(e)=$employeeID AND elementId(m)=$movieID CREATE (e)-[w:WORK_ON {role: $role}]->(m)'
        with self.driver.session() as session:
            session.run(query, employeeID=empl_id, movieID=movie_id, role=role)
    
    def get_movie_crew(self, id):
        query = 'MATCH (e:Employee)-[w:WORK_ON]->(m:Movie) WHERE elementId(m)=$movieID return w.role, e'
        with self.driver.session() as session:
            return session.run(query, movieID=id).values()

    def get_employee_movies(self, id):
        query = 'MATCH (e:Employee)-[w:WORK_ON]->(m:Movie) WHERE elementId(e)=$employeeID return w.role, m'
        with self.driver.session() as session:
            return session.run(query, employeeID=id).values()

    def filter_db(self, role, rating, age, name, surname, title, premiere, top, sort):
        query = 'MATCH (e:Employee)-[w:WORK_ON]->(m:Movie)'
        where = []
        inputs = {}
        if role != 'None':
            where.append('w.role=$role')
            inputs.setdefault('role', role)

        if rating != 'None':
            where.append('m.rating>$lowRating AND m.rating<=$highRating')
            print(rating)
            inputs.setdefault('lowRating', float(rating)-1)
            inputs.setdefault('highRating', float(rating))

        if age != 'None':
            where.append('e.age>$lowAge AND e.age<=$highAge')
            inputs.setdefault('lowAge', int(age)-10)
            inputs.setdefault('highAge', int(age))

        if name != '':
            where.append('e.name=$name')
            inputs.setdefault('name', name)

        if surname != '':
            where.append('e.surname=$surname')
            inputs.setdefault('surname', surname)

        if title != '':
            where.append('m.title=$title')
            inputs.setdefault('title', title)

        try:
            tmp = int(premiere)
            where.append('m.premiere.year=$premiere')
            inputs.setdefault('premiere', tmp)
        except ValueError:
            pass

        where = ' AND '.join(where)
        if where:
            query += ' WHERE ' + where
        query += ' RETURN e, w.role, m'

        if sort in ['name', 'surname']:
            query += ' ORDER BY e.'+sort
        elif sort in ['title', 'rating']:
            query += ' ORDER BY e.'+sort

        try:
            tmp = int(top)
            query += ' LIMIT '+str(tmp)
        except ValueError:
            pass

        with self.driver.session() as session:
            return session.run(query, inputs).values()

    def remove_employee(self, id):
        query = 'MATCH (e:Employee) WHERE elementId(e)=$employeeID DETACH DELETE e'
        with self.driver.session() as session:
            session.run(query, employeeID=id)

    def get_employee(self, id):
        query = 'MATCH (e:Employee) WHERE elementId(e)=$employeeID RETURN e'
        with self.driver.session() as session:
            return session.run(query, employeeID=id).single()[0]

    def update_person(self, id, name, surname, age):
        query = 'MATCH (e:Employee) WHERE elementId(e)=$employeeID SET e.name=$name, e.surname=$surname, e.age=$age'
        with self.driver.session() as session:
            session.run(query, employeeID=id, name=name, surname=surname, age=int(age))

    def remove_movie(self, id):
        query = 'MATCH (m:Movie) WHERE elementId(m)=$movieID DETACH DELETE m'
        with self.driver.session() as session:
            session.run(query, movieID=id)

    def get_movie(self, id):
        query = 'MATCH (m:Movie) WHERE elementId(m)=$movieID RETURN m'
        with self.driver.session() as session:
            return session.run(query, movieID=id).single()[0]

    def update_movie(self, id, title, premiere, rating):
        query = 'MATCH (m:Movie) WHERE elementId(m)=$movieID SET m.title=$title, m.premiere=$premiere, m.rating=$rating'
        with self.driver.session() as session:
            session.run(query, movieID=id, title=title, premiere=premiere, rating=float(rating))