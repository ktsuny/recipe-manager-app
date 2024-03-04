
from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random')
def random_number():
    number = random.randint(1, 100)  # Generates a random number between 1 and 100
    return jsonify({'number': number})

if __name__ == '__main__':
    app.run(port=5001)
