from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import data
import database

app = Flask(__name__)

tripitems = [{"name": "Walmart", "address": "2100 Nueces Road 19493"}]
dataclass = data.DataClass()

@app.route('/')
def home():
    return render_template("home.html", trips = database.getalltrips())

@app.route('/addtrip', methods = ['POST', 'GET'])
def addtrip():
    name = request.form.get("tripname")
    creator = 'Bob'
    numitems = '0'
    database.inserttrip(name, creator, numitems)
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
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = tripitems, trip = name.upper())
    if dataclass.getsearch() != None:
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = tripitems, trip = name.upper())
    else:
        return render_template("trip_details.html", search_result = None, tripitems = tripitems, trip = name.upper())

@app.route('/addtripitem', methods = ['POST', 'GET'])
def addtripitem():
    new_item = json.loads(request.form['output'])
    tripitems.append(new_item)
    itemlist = {
        "items" : tripitems
    }
    return jsonify(itemlist)

@app.route('/deletetripitem', methods = ['POST', 'GET'])
def deletetripitem():
    delete_item = json.loads(request.form['output'])
    for i in range(len(tripitems)):
        if tripitems[i]['address'] == delete_item['address']:
            del tripitems[i]
            break
    itemlist = {
        "items": tripitems
    }
    return jsonify(itemlist)

if __name__=="__main__":
    app.run(debug=True)