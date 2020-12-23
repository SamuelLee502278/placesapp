from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import data
import database

app = Flask(__name__)

tripitems = ["Samuel Lee", "Chicken", "Lol"]
dataclass = data.DataClass()

@app.route('/')
def home():
    return render_template("home.html", trips = database.getalltrips())

@app.route('/addtrip', methods = ['POST', 'GET'])
def addtrip():
    name = request.form.get("tripname")
    name = name.split()
    name = [x.capitalize() for x in name]
    name = " ".join(name)
    creator = 'Bob'
    database.inserttrip(name, creator)
    return redirect(url_for('home'))

@app.route('/<string:name>/deletetrip', methods = ['POST', 'GET'])
def deletetrip(name):
    database.deletetrip(name)
    return redirect(url_for('home'))

@app.route('/<string:name>/tripdetails',methods = ['POST','GET'])
def tripdetails(name):
    if request.method == 'POST':
        result_string = request.form.get("place")
        result_array = dataclass.findplace(result_string)
        dataclass.storesearch(result_array)
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = database.getalltripitems(), trip = name)
    if dataclass.getsearch() != None:
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = database.getalltripitems(), trip = name)
    else:
        return render_template("trip_details.html", search_result = None, tripitems = database.getalltripitems(), trip = name)

@app.route('/addtripitem', methods = ['POST', 'GET'])
def addtripitem():
    new_item = json.loads(request.form['output'])
    database.inserttripitem(new_item['tripname'], new_item['name'], new_item['address'], new_item['lat'], new_item['lng'])
    return "success"

@app.route('/deletetripitem', methods = ['POST', 'GET'])
def deletetripitem():
    delete_item = json.loads(request.form['output'])
    print(delete_item['address'])
    database.deletetripitem(delete_item['address'])
    return "success"

if __name__=="__main__":
    app.run(debug=True)