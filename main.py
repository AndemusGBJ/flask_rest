# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flaskext.mysql import MySQL

main = Flask(__name__)
api = Api(main)



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

"""
Utilisation de MySql avec Flaskrestful.
On crée un utilisateur avec un email et un password
"""
class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            return {'Email': args['email'], 'Password': args['password']}

        except Exception as e:
            return {'error': str(e)}


        mysql = MySQL()
        # MySQL configurations
        main.config['MYSQL_DATABASE_USER'] = 'roor'
        main.config['MYSQL_DATABASE_PASSWORD'] = '44114411Ab#'
        main.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
        main.config['MYSQL_DATABASE_HOST'] = 'localhost'

        mysql.init_app(main)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('spCreateUser',(_userEmail, _userPassword))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return {'StatusCode': '200', 'Message': 'User creation success'}
        else:
            return {'StatusCode': '1000', 'Message': str(data[0])}


api.add_resource(listeEtudiants, '/etudiants')
api.add_resource(Etudiant, '/etudiants/<string:matricule>')
api.add_resource(CreateUser, '/CreateUser')



if __name__ == '__main__':
    main.run(debug=True, port=8000)

