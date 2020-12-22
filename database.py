import pymysql
import config as creds

conn = pymysql.connect(
    host = creds.host,
    port = creds.port,
    user = creds.user,
    password = creds.password,
    db = "placesapp"
)

cursor = conn.cursor()

#Created Trips Table
# createtable = "CREATE TABLE Trips(name varchar(200) PRIMARY KEY, creator varchar(200), numitems varchar(10))"
# cursor.execute(createtable)

def inserttrip(nametrip, creatorname, items):
    insertquery = "INSERT INTO Trips (name, creator, numitems) VALUES (%s , %s, %s)"
    cursor.execute(insertquery, (nametrip, creatorname, items))
    conn.commit()

def deletetrip(tripname):
    deletequery = "DELETE FROM Trips WHERE name = %s" 
    cursor.execute(deletequery, (tripname))
    conn.commit()

def getalltrips():
    allquery = "SELECT * FROM Trips"
    cursor.execute(allquery)
    alltrips = cursor.fetchall()
    return alltrips




