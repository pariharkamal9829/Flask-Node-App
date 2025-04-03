Step 1: Create a Project Folder
Create a new folder for your project and navigate into it:


mkdir Flask-Node-App

cd Flask-Node-App


Inside this folder, create two subdirectories:


mkdir frontend backend


 Step 2: Setup Flask Backend

Navigate into the backend folder:


cd backend


1 Install Flask and Dependencies
Create a virtual environment:


python -m venv venv


Install Flask and dependencies:


pip install flask flask-cors pymongo






2️ Create app.py
Inside the backend folder, create app.py:

from flask import Flask, request, jsonify

from flask_cors import CORS

import pymongo

import os


app = Flask(__name__)

CORS(app)


# Connect to MongoDB Atlas

MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/myDatabase?retryWrites=true&w=majority"

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



3️ Create requirements.txt

pip freeze > requirements.txt



4️ Create Dockerfile for Flask
Inside the backend folder, create a Dockerfile:


# Use official Python image

FROM python:3.9


# Set working directory

WORKDIR /app


# Copy files to container

COPY . .


# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt


# Expose Flask port

EXPOSE 5000


# Run Flask app

CMD ["python", "app.py"]



 Step 3: Setup Node.js Frontend
Navigate back to the root directory and into the frontend folder:


cd ../frontend


1️ Initialize a Node.js Project

npm init -y


2️ Install Express and Axios

npm install express axios cors body-parser



3️ Create server.js
Inside the frontend folder, create server.js

const express = require("express");

const axios = require("axios");

const cors = require("cors");

const bodyParser = require("body-parser");


const app = express();

app.use(cors());

app.use(bodyParser.json());


app.get("/", (req, res) => {

    res.send(`

        <form action="/submit" method="post">

            <input type="text" name="name" placeholder="Item Name" required />

            <input type="text" name="description" placeholder="Item Description" required />

            <button type="submit">Submit</button>

        </form>

    `);

});


app.post("/submit", async (req, res) => {

    try {

        const response = await axios.post("http://backend:5000/submit", req.body);

        res.send("<h1>Data submitted successfully</h1>");

    } catch (error) {

        res.send(`<h1>Error: ${error.message}</h1>`);

    }

});


const PORT = 3000;

app.listen(PORT, () => {

    console.log(`Frontend running on http://localhost:${PORT}`);

});



4️ Create Dockerfile for Node.js
Inside the frontend folder, create a Dockerfile:


# Use official Node.js image

FROM node:18


# Set working directory

WORKDIR /app


# Copy package.json and install dependencies

COPY package*.json ./

RUN npm install


# Copy the rest of the application

COPY . .


# Expose port

EXPOSE 3000


# Start the server

CMD ["node", "server.js"]



📌 Step 4: Create docker-compose.yml
Navigate back to the root project folder and create docker-compose.yml:


version: "3.8"


services:

  backend:

    build: ./backend

    ports:

      - "5000:5000"

    networks:

      - app_network


  frontend:

    build: ./frontend

    ports:

      - "3000:3000"

    depends_on:

      - backend

    networks:

      - app_network


networks:

  app_network:

    driver: bridge



 Step 5: Build and Run Docker Containers
Navigate to the project root and run:

docker-compose up --build




Now, visit:

Frontend: http://localhost:3000


Backend API: http://localhost:5000/api


 Step 6: Push Images to Docker Hub
1️ Login to Docker Hub

docker login


2️ Tag and Push Backend Image

docker tag flask-backend kamal9829/flask-backend

docker push kamal9829/flask-backend





3️ Tag and Push Frontend Image

docker tag node-frontend kamal9829/node-frontend

docker push kamal9829/node-frontend




Step 7: Push Code to GitHub

1️ Initialize Git and Create Repository

git init

git remote add origin git@github.com:pariharkamal9829/Flask-Node-App.git

2️ Add .gitignore
Create .gitignore in the root folder:


node_modules

.vscode

.env

venv

__pycache__


3️ Commit and Push Code
git add .

git commit -m "Initial commit: Flask-Node app with Docker"

git branch -M main

git push -u origin main


