from flask import *
from pymongo import MongoClient
from multiprocessing import Manager

'''
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection
test_id = collection.insert_one(test_data).inserted_id
print(collection.find_one(test_id))
'''

alive_clients = Manager().list()

app = Flask(__name__, static_folder='static')


def isIdValid(id):
    return not id in alive_clients[:]

@app.route('/')
def return_site():
    return render_template('index.html')

@app.route('/baduser')
def bad_user():
    return render_template('baduser.html')

@app.route('/gooduser')
def good_user():
    return render_template('gooduser.html')

@app.route('/route/<id>')
def checkId(id):
    if isIdValid(id):
        alive_clients.append(id)
        print(alive_clients)
        return render_template("gooduser.html", ID = id)
    return redirect("http://space.brothersproduction.ru:303/baduser", code = 302)

@app.route('/wgl_player')
def wgl_player():
    return true

@app.route('/post', methods = ['POST'])
def post():
    print(alive_clients)
    print(str(request.form['ID']))
    alive_clients.remove(str(request.form['ID']).strip())
    return jsonify(success=True)

app.run('0.0.0.0', '303')
