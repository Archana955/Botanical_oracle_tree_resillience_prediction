from flask import Flask, request, render_template, url_for
import pickle
import numpy as np
import json
import requests




app = Flask(__name__)

# Load the model with specific dtype
with open('gradient_boosting_classifier.pkl', 'rb') as file:
    try:
        model = pickle.load(file, encoding='latin1')  # Specify encoding for Python 2 compatibility
    except ValueError as e:
        # Handle dtype mismatch error
        print(f"ValueError: {e}")
        model = None  # Set model to None or handle the error accordingly
# Map encoded species values to species names
species_mapping = {
    0: 'Acer saccharum',
    1: 'Prunus serotina',
    2: 'Quercus alba',
    3: 'Quercus rubra'
}


@app.route("/")
def f():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("index.html")

@app.route("/inspect")
def inspect():
    return render_template("inner-page.html")

@app.route('/home')
def home():
    return render_template("index.html")


@app.route("/output", methods=["GET", "POST"])
def output():
    if request.method == 'POST':
        var1 = request.form["Species"]
        var2 = request.form["Myco"]
        var3 = request.form["AMF"]
        var4 = request.form["Phenolics"]
        var5 = request.form["Lignin"]
        var6 = request.form["NSC"]
        var7 = request.form["Time"]
        

        # Convert the input data into a numpy array
        predict_data = np.array([var1, var2, var3, var4, var5, var6, var7]).reshape(1, -1)

        # Use the loaded model to make predictions
        predict = model.predict(predict_data)

        if (predict == 1):
            return render_template('output.html', predict="Survived")
        else:
            return render_template('output.html', predict="Not Survived")
    return render_template("output.html")

if __name__ =="__main__":
    app.run(debug=True,port =6066)