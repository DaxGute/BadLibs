from flask import Flask
from flask import jsonify
from getNewTitle import getNewTitle

app = Flask(__name__)

@app.route('/')
def index():
    dictionary = {'message': getNewTitle()}
    return jsonify(dictionary)

if __name__ == '__main__':
    app.run(debug=True)