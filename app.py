from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import data

app = Flask(__name__)

array = ["california", "texas"]
tripitems = [{"name": "Walmart", "address": "1619 Heddon Falls Dr."}]
dataclass = data.DataClass()

@app.route('/')
def home():
    #load current database with trips
    return render_template("home.html", trips = array)

@app.route('/trip')
def trip():
    #when user clicks on trip, routes to the trip instance page
    return render_template("trip.html")

@app.route('/add', methods = ['POST', 'GET'])
def addtrip():
    array.append(request.form.get("tripname"))
    return redirect(url_for('home'))

@app.route('/tripdetails',methods = ['POST','GET'])
def tripdetails():
    if request.method == 'POST':
        result_string = request.form.get("place")
        result_array = dataclass.findplace(result_string)
        dataclass.storesearch(result_array)
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = tripitems)
    if dataclass.getsearch() != None:
        return render_template("trip_details.html", search_result = dataclass.getsearch(), tripitems = tripitems)
    else:
        return render_template("trip_details.html", search_result = None, tripitems = tripitems)

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