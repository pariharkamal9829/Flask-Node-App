from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin@clustrflask.jifwgcj.mongodb.net/?retryWrites=true&w=majority&appName=clustrflask"
client = pymongo.MongoClient(MONGO_URI)
db = client["todo_app"]
collection = db["tasks"]

@app.route('/api', methods=['GET'])
def get_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route('/submit', methods=['POST'])
def submit_task():
    data = request.json
    if "name" in data and "description" in data:
        collection.insert_one(data)
        return jsonify({"message": "Data submitted successfully"}), 201
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
