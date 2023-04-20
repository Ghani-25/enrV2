from flask import Flask, request, jsonify, render_template
import pandas as pd
from model import enrichir

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    text = request.form.get("occupations")
    occupation = text.split('.')
    print(occupation)
    output = enrichir(occupation)

    return render_template('index.html', prediction_text='Enriched prospects $ {}'.format(output))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    occupation = data.get("occupations")
    print(occupation)
    output = enrichir(occupation)

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
