# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
import requests



app = Flask(__name__)
api = Api(app)



ETUDIANTS = {


    'MK001': { 'nom': 'Etudiant 1','prenom':'Etudiant x'},
    'MK002': { 'nom': 'Etudiant 2','prenom':'Etudiant x'},
    'MK003': { 'nom': 'Etudiant 3','prenom':'Etudiant x'},
    'MK004': { 'nom': 'Etudiant 4','prenom':'Etudiant x'},
    'MK005': { 'nom': 'Etudiant 5','prenom':'Etudiant x'}
}

parser = reqparse.RequestParser()
parser.add_argument('nom')
parser.add_argument('prenom')

class listeEtudiants(Resource):
    def get(self):
        return ETUDIANTS

class Etudiant(Resource):
    def get(self, matricule):
        if matricule not in ETUDIANTS:
            abort(404, message= f'Le matricule {matricule} est incorrect')
        return ETUDIANTS[matricule]

    def post(self, matricule):

        if matricule not in ETUDIANTS:
            abort(409, message=f'Le matricule {matricule} existe déjà')
        arguments = parser.parse_args()
        nom = arguments['nom']
        prenom = arguments['prenom']
        ETUDIANTS[matricule]={'nom': nom, 'prenom':prenom}

        return ('Created', 201)

    def delete(self,matricule):

        if matricule not in ETUDIANTS:
            abort(409, message=f'Le matricule {matricule} existe n\'est pas dans la liste')
        del ETUDIANTS[matricule]
        return ('Supprimé avec succsès', 200)

    def put(self,matricule):
        if matricule not in ETUDIANTS:
            abort(409, message=f'Le matricule {matricule} n\'existe pas')

        arguments = parser.parse_args()
        nom = arguments['nom']
        prenom = arguments['prenom']
        ETUDIANTS[matricule].update({'nom': nom, 'prenom': prenom})

        return ('Modifié avec succès', 200)

class TextSimilarity(Resource):
    def post(self):

        url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/text_similarity/"

        payload = "text1=The%20hippocampus%20is%20a%20major%20component%20of%20the%20brains%20of%20humans%20and%20other%20vertebrates.%20It%20belongs%20to%20the%20limbic%20system%20and%20plays%20important%20roles%20in%20the%20consolidation%20of%20information%20from%20short-term%20memory%20to%20long-term%20memory%20and%20spatial%20navigation.%20Humans%20and%20other%20mammals%20have%20two%20hippocampi%2C%20one%20in%20each%20side%20of%20the%20brain.%20The%20hippocampus%20is%20a%20part%20of%20the%20cerebral%20cortex%3B%20and%20in%20primates%20it%20is%20located%20in%20the%20medial%20temporal%20lobe%2C%20underneath%20the%20cortical%20surface.%20It%20contains%20two%20main%20interlocking%20parts%3A%20Ammon's%20horn%20and%20the%20dentate%20gyrus.&text2=An%20important%20part%20of%20the%20brains%20of%20humans%20and%20other%20vertebrates%20is%20the%20hippocampus.%20It's%20part%20of%20the%20limbic%20system%20and%20moves%20information%20from%20short-term%20to%20long-term%20memory.%20It%20also%20helps%20us%20move%20around.%20Humans%20and%20other%20mammals%20have%20two%20hippocampi%2C%20one%20on%20each%20side.%20The%20hippocampus%20is%20a%20part%20of%20the%20cerebral%20cortex%3B%20and%20in%20primates%20it%20is%20found%20in%20the%20medial%20temporal%20lobe%2C%20beneathe%20the%20cortical%20surface.%20It%20has%20two%20main%20interlocking%20parts%3A%20Ammon's%20horn%20and%20the%20dentate%20gyrus."
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'x-rapidapi-key': "4dfeb488c9mshdeac92794c046a8p113fecjsn63f0f1bec84a",
            'x-rapidapi-host': "twinword-twinword-bundle-v1.p.rapidapi.com"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return (response.text)



api.add_resource(listeEtudiants, '/etudiants')
api.add_resource(Etudiant, '/etudiants/<string:matricule>')
api.add_resource(TextSimilarity, '/Text')





if __name__ == '__main__':
    app.run(debug=True, port=8000)



