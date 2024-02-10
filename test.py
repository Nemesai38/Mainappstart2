import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("SELECT * FROM Personnel_Info")
r = c.fetchall()

print(r[0][2])

i = 0
data = r[i]

print(len(data))
    
    

