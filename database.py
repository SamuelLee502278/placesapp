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
# createtable = "CREATE TABLE Trips(name varchar(200) PRIMARY KEY, creator varchar(200), numitems INT)"
# createtable = "CREATE TABLE TripItems(tripname varchar(200), placename varchar(200), address varchar(200) PRIMARY KEY, lattitude varchar(200), longitude varchar(200), rating varchar(10), price varchar(10), phone varchar(20), website varchar(200))"
# cursor.execute(createtable)

def inserttrip(nametrip, creatorname):
    if nametrip == "":
        return "noname"
    insertquery = "INSERT INTO Trips (name, creator, numitems) VALUES (%s , %s, 0)"
    try:
        cursor.execute(insertquery, (nametrip, creatorname))
        conn.commit()
        return "success"
    except pymysql.Error:
        return "duplicate"

def modifynumitems(nametrip):
    modifyquery = "UPDATE Trips SET numitems = "

def deletetrip(tripname):
    deletequery = "DELETE FROM Trips WHERE name = %s" 
    cursor.execute(deletequery, (tripname))
    conn.commit()

def getalltrips():
    allquery = "SELECT * FROM Trips"
    cursor.execute(allquery)
    alltrips = cursor.fetchall()
    return alltrips

def inserttripitem(tripname, placename, address, lat, lng, rating, price, phone, website):
    insertquery = "INSERT INTO TripItems (tripname, placename, address, lattitude, longitude, rating, price, phone, website) VALUES (%s , %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(insertquery, (tripname, placename, address, lat, lng, rating, price, phone, website))
        conn.commit()
        return "success"
    except pymysql.Error:
        return "error"

def deletetripitem(address):
    deletequery = "DELETE FROM TripItems WHERE address = %s" 
    cursor.execute(deletequery, address)
    conn.commit()

def getalltripitems(tripname):
    turntolist = []
    allquery = "SELECT * FROM TripItems WHERE tripname = %s"
    cursor.execute(allquery, tripname)
    alltrips = cursor.fetchall()
    for trips in alltrips:
        turntolist.append(list(trips))
    return turntolist

def getindividualtrip(address):
    getquery = "SELECT * FROM TripItems WHERE address = %s LIMIT 1"
    cursor.execute(getquery, address)
    gettrip = cursor.fetchall()
    return gettrip


# def getcoordinates(name):
#     getcordquery = "SELECT 



