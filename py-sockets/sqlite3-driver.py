import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE if not exists plants
	(commonName text, plantStatus text, dateAdded date)''')

# Insert a row of data
# c.execute("INSERT INTO plants VALUES ('chili pepper','healthy','2018-01-05')")

# Save (commit) the changes
conn.commit()

# retrieve data
for row in c.execute('SELECT * FROM plants ORDER BY dateAdded'):
	print(row)

# close the connection when you are done
# changes need to be committed before closing or they will be lost
conn.close()
