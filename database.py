import pymysql
import json
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
# createtable = "CREATE TABLE TripItems(tripname varchar(200), placename varchar(200), address varchar(200), lattitude varchar(200), longitude varchar(200), CONSTRAINT trip_entry PRIMARY KEY (tripname,address))"
# createtable = "CREATE TABLE PlaceDetails(address varchar(200) PRIMARY KEY, id varchar(200), rating varchar(10), price varchar(10), phone varchar(20), website varchar(200), photo1 varchar(200), photo2 varchar(200), photo3 varchar(200), hours varchar(2000))"
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

def addnumitems(nametrip):
    getnumitemsquery = "SELECT numitems FROM Trips WHERE name = %s"
    cursor.execute(getnumitemsquery, nametrip)
    numitems = cursor.fetchone()
    addone = numitems[0] + 1
    addnumitemsquery = "UPDATE Trips SET numitems = %s WHERE name = %s"
    cursor.execute(addnumitemsquery, (addone, nametrip))
    conn.commit()

def deletenumitems(nametrip):
    getnumitemsquery = "SELECT numitems FROM Trips WHERE name = %s"
    cursor.execute(getnumitemsquery, nametrip)
    numitems = cursor.fetchone()
    addone = numitems[0] + -1
    addnumitemsquery = "UPDATE Trips SET numitems = %s WHERE name = %s"
    cursor.execute(addnumitemsquery, (addone, nametrip))
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

def inserttripitem(new_item, yelpinfo):
    insertplace = "INSERT INTO TripItems (tripname, placename, address, lattitude, longitude) VALUES (%s, %s, %s, %s, %s)"
    insertdetails = "INSERT INTO PlaceDetails (address, id, rating, price, phone, website, photo1, photo2, photo3, hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(insertdetails, (new_item['address'], yelpinfo['id'], yelpinfo['rating'], yelpinfo['price'], yelpinfo['phone'], yelpinfo['website'], yelpinfo['photo1'], yelpinfo['photo2'], yelpinfo['photo3'], json.dumps(yelpinfo['hours'])))
        conn.commit()
    except pymysql.Error:
        pass
    try:
        cursor.execute(insertplace, (new_item['tripname'], new_item['name'], new_item['address'], new_item['lat'], new_item['lng']))
        conn.commit()
        return "success"
    except pymysql.Error:
        return "error"

def deletetripitem(address,tripname):
    deletequery = "DELETE FROM TripItems WHERE address = %s AND tripname = %s" 
    cursor.execute(deletequery, (address,tripname))
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
    getquery = "SELECT TripItems.lattitude, TripItems.longitude, PlaceDetails.address, PlaceDetails.rating, PlaceDetails.price, PlaceDetails.phone, PlaceDetails.website, PlaceDetails.photo1, PlaceDetails.photo2, PlaceDetails.photo3, PlaceDetails.hours FROM TripItems INNER JOIN PlaceDetails ON TripItems.address = PlaceDetails.address WHERE TripItems.address = %s"
    cursor.execute(getquery, address)
    gettrip = cursor.fetchall()
    return gettrip
