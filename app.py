from flask import Flask, render_template, request, redirect, url_for
import data

app = Flask(__name__)

array = ["california", "texas"]
tripitems = [{"name": "Walmart", "address": "1619 Heddon Falls Dr."}]

@app.route('/')
def home():
    #load current database with trips
    return render_template("home.html", trips = array)

@app.route('/trip')
def trip():
    #when user clicks on trip, routes to the trip instance page
    return render_template("trip.html")

@app.route('/tripdetails',methods = ['POST','GET'])
def tripdetails():
    if request.method == 'POST':
        result_string = request.form.get("place")
        result_array = data.findplace(result_string)
        return render_template("trip_details.html", search_result = result_array, tripitems = tripitems)
    return render_template("trip_details.html", search_result = None, tripitems = tripitems)

@app.route('/add', methods = ['POST', 'GET'])
def addtrip():
    array.append(request.form.get("tripname"))
    return redirect(url_for('home'))

@app.route('/addtripitem', methods = ['POST', 'GET'])
def addtripitem():
    # search = request.args.get('text')
    # print(search)
    print("hello")
    return redirect(url_for('home'))


# @app.route('/delete', methods = ['POST', 'GET'])
# def delete():

if __name__=="__main__":
    app.run(debug=True)