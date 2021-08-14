import json
import sqlite3

conn =sqlite3.connect("roster.sqlite")
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

filename = input("Enter the filename")
if len(filename) < 1 :
    filename = 'roster_data.json'

str_data = open(filename).read()
# converting the string data form of json into python list
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('''INSERT OR IGNORE INTO User(name)
    VALUES (?)''', (name,))
    cur.execute('''SELECT id FROM User WHERE name = ? '''
    , (name,))
    user_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR IGNORE INTO Course(title)
    VALUES (?)''' , (title,))
    cur.execute('''SELECT id FROM Course WHERE title = ? '''
    , (title,))
    course_id = cur.fetchone()[0]

    cur.execute(''' INSERT OR REPLACE INTO Member(user_id ,
    course_id , role) VALUES (?,?,?)''',(user_id,course_id,role))

#committing the new values in the end of the loop
#in order to speed up process
conn.commit()

sqlstr = '''SELECT User.name,Course.title, Member.role FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2 '''

#this code will show the first step of the solution that
for row in cur.execute(sqlstr):
    print(str(row[0]),str(row[1]),str(row[2]))

sqlstr2 = '''SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1 '''

for row in cur.execute(sqlstr2):
    #this code will show the correct answer of the assignment.
    print(str(row[0]))
