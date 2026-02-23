import psycopg2
import csv

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='student_db',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                grade VARCHAR(10) NOT NULL
            )
        ''')
        self.conn.commit()

    def add_student(self, name, grade):
        self.cur.execute('INSERT INTO students (name, grade) VALUES (%s, %s)', (name, grade))
        self.conn.commit()

    def get_students(self):
        self.cur.execute('SELECT * FROM students')
        return self.cur.fetchall()

    def update_student(self, id, name, grade):
        self.cur.execute('UPDATE students SET name=%s, grade=%s WHERE id=%s', (name, grade, id))
        self.conn.commit()

    def delete_student(self, id):
        self.cur.execute('DELETE FROM students WHERE id=%s', (id,))
        self.conn.commit()

    def search_by_name(self, name):
        self.cur.execute('SELECT * FROM students WHERE name ILIKE %s', ('%' + name + '%',))
        return self.cur.fetchall()

    def search_by_grade(self, grade):
        self.cur.execute('SELECT * FROM students WHERE grade = %s', (grade,))
        return self.cur.fetchall()

    def search_by_id(self, id):
        self.cur.execute('SELECT * FROM students WHERE id = %s', (id,))
        return self.cur.fetchone()

    def export_to_csv(self, filename):
        students = self.get_students()
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Grade'])
            writer.writerows(students)

    def close(self):
        self.cur.close()
        self.conn.close()