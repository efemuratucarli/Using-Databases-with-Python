import sqlite3
import urllib.request
import ssl


#connecting to the file or creating a file to store our database
conn = sqlite3.connect("emailtable.sqlite")

#creating a cursor to execute sql commands.
cur = conn.cursor()

#deleting any possible table whose tablename is Counts
cur.execute("DROP TABLE IF EXISTS Counts")

#creating a new table
cur.execute("CREATE TABLE Counts(org TEXT,count INTEGER)")

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "mbox.txt"

#opening the file
fhandle = open(fname)

#starting to read it line by line
for line in fhandle:
    #finding the email address and spliting it into name and
    #domain(organization)
    if not line.startswith("From "):
        continue
    parts = line.split()
    email = parts[1]

    #assigning the organization name to the domain variable
    domain = email.split("@")[1]

    #indicating the correct column for the organization
    cur.execute("SELECT count FROM Counts WHERE org = ?",(domain,))
    #assigning the data in the selected org column to the value variable
    value = cur.fetchone()

    #updating the organization column for the selected domain
    if value is None:
        cur.execute('''INSERT INTO Counts (org,count) VALUES
        (?,1)''', (domain,))
    else:
        cur.execute('''UPDATE Counts SET count = count + 1 WHERE org = ?
        ''',(domain,))

#Committing the modified form of the database after the changes
#to speed up the execution
conn.commit()

#Obtaning the results that have ordered by count
sqlstr = 'SELECT org, count FROM Counts ORDER BY count'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

#closing the database
cur.close()
