from flask import Flask, render_template, request, redirect, url_for
import data

app = Flask(__name__)

array = ["california", "texas"]

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
        return render_template("trip_details.html", result = result_array)
    return render_template("trip_details.html", result = "")

@app.route('/add', methods = ['POST', 'GET'])
def add():
    array.append(request.form.get("tripname"))
    return redirect(url_for('home'))

# @app.route('/delete', methods = ['POST', 'GET'])
# def delete():

if __name__=="__main__":
    app.run(debug=True)