from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import data
import database
import utility
import config as creds

app = Flask(__name__)

dataclass = data.DataClass()
utility = utility.UtilityClass()

@app.route('/')
def home():
    return render_template("home.html", trips = database.getalltrips())

@app.route('/addtrip', methods = ['POST', 'GET'])
def addtrip():
    newtrip = json.loads(request.form['output'])
    returnstring = database.inserttrip(utility.capitalizeinput(newtrip['tripname']), utility.capitalizeinput(newtrip['creator']))
    if returnstring == "success":
        return "success"
    elif returnstring == "duplicate":
        return "duplicate"
    elif returnstring == "noname":
        return "noname"

@app.route('/<string:name>/deletetrip')
def deletetrip(name):
    database.deletetrip(name)
    return redirect(url_for('home'))

@app.route('/<string:name>/tripdetails',methods = ['POST','GET'])
def tripdetails(name):
    if request.method == 'POST':
        result_string = request.form.get("place")
        result_array = dataclass.findplace(result_string)
        dataclass.storesearch(result_array)
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = database.getalltripitems(name), trip = name)
    if dataclass.getsearch() != None:
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = database.getalltripitems(name), trip = name)
    else:
        return render_template("trip_details.html", search_result = None, tripitems = database.getalltripitems(name), trip = name)

@app.route('/addtripitem', methods = ['POST', 'GET'])
def addtripitem():
    new_item = json.loads(request.form['output'])
    yelpinfo = dataclass.get_businessearch(new_item)
    returnstring = database.inserttripitem(new_item, yelpinfo)
    if returnstring == "success":
        database.addnumitems(new_item['tripname'])
        return "success"
    else:
        return "error"

@app.route('/deletetripitem', methods = ['POST', 'GET'])
def deletetripitem():
    delete_item = json.loads(request.form['output'])
    database.deletetripitem(delete_item['address'])
    database.deletenumitems(delete_item['tripname'])
    return "success"

@app.route('/<string:address>/placedetail')
def placedetail(address):
    getplace = database.getindividualtrip(address)
    hours_operation = utility.operation_hours(json.loads(getplace[0][10])[0])
    return render_template("place_detail.html", creds = creds.secret, place = getplace[0], hours = hours_operation)

if __name__=="__main__":
    app.run(debug=True)