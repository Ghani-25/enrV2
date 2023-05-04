from flask import Flask, request, jsonify, render_template
import pandas as pd
from model import enrichir
import json
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://goulag:9eKA5GfkeqbTTEu8@cluster5.2qw5j.mongodb.net/Goulag?retryWrites=true&w=majority")
db = client["Goulag"]

# récupérer une référence à la collection contenant les profils
profils_collection = db["profiles"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get("occupations")
    occupation = text.split('.')
    print(occupation)
    output = enrichir(occupation, 1000)

    return render_template('index.html', prediction_text=output)

@app.route('/retrieve_ids', methods=['POST'])
def retrieve_ids():
    # Étape 1: Récupérez les identifiants à partir du formulaire POST
    ids_string = request.form['ids']
    ids = json.loads(ids_string)

    # Étape 2: Récupérez les utilisateurs de la base de données MongoDB en utilisant les identifiants
    retrieved_users = profils_collection.find({"_id": {"$in": [ObjectId(user_id) for user_id in ids]}})

    # Étape 3: Pas besoin d'appeler la fonction enrichir ici

    # Étape 4: Passez la liste des utilisateurs à la fonction render_template
    return render_template('results.html', users=retrieved_users)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/results', methods=['POST'])
def results():
    if request.method == 'GET':
        return jsonify({"error": "Please send a JSON object with the 'occupations' key in the request body"}), 400

    try:
        data = request.get_json(force=True)
        occupation = data.get("occupations")
        count = data.get("count")
        print(occupation)
        output = enrichir(occupation, count)

        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": "Invalid JSON object", "message": str(e)}), 400


@app.route('/results_html', methods=['POST'])
def results_html():
    if request.method == 'GET':
        return jsonify({"error": "Please send a JSON object with the 'occupations' key in the request body"}), 400

    try:
        data = request.get_json(force=True)
        occupation = data.get("occupations")
        count = data.get("count")

        # Appel de la fonction enrichir pour récupérer les profils correspondants
        profiles = enrichir(occupation, count)

        # Récupération des résultats à partir de la base de données MongoDB
        retrieved_users = profils_collection.find({"_id": {"$in": [ObjectId(user_id) for user_id in profiles.keys()]}})

        # Création d'une liste contenant les profils enrichis et leurs scores correspondants
        enriched_users = []
        for user in retrieved_users:
            user_id = str(user["_id"])
            user_score = profiles[user_id]
            user["score"] = user_score
            enriched_users.append(user)

        # Renvoyer les résultats à la page HTML via le template results.html
        return render_template('results.html', users=enriched_users)

    except ValueError as e:
        return jsonify({"error": "Invalid JSON object", "message": str(e)}), 400



if __name__ == "__main__":
    app.run(debug=True)
