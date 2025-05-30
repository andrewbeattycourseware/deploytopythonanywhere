from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

from bookDAO import bookDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return "Hello, World!"

#curl "http://127.0.0.1:5000/books"
@app.route('/books')
@cross_origin()
def getAll():
    #print("in getall")
    results = bookDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/books/2"
@app.route('/books/<int:id>')
@cross_origin()
def findById(id):
    foundBook = bookDAO.findByID(id)

    return jsonify(foundBook)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/books', methods=['POST'])
@cross_origin()
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    book = {
        "title": request.json['title'],
        "author": request.json['author'],
        "price": request.json['price'],
    }
    addedbook = bookDAO.create(book)
    
    return jsonify(addedbook)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    foundBook = bookDAO.findByID(id)
    if not foundBook:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'title' in reqJson:
        foundBook['title'] = reqJson['title']
    if 'author' in reqJson:
        foundBook['author'] = reqJson['author']
    if 'price' in reqJson:
        foundBook['price'] = reqJson['price']
    bookDAO.update(id,foundBook)
    return jsonify(foundBook)
        

    

@app.route('/books/<int:id>' , methods=['DELETE'])
@cross_origin()
def delete(id):
    bookDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)
