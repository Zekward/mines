from flask import Flask, render_template, request, redirect, url_for, session
import webbrowser
from pymongo import MongoClient
from threading import Timer
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
client = MongoClient(os.environ.get('MONGO_URI'))
db = client["mines"]
user_collection = db["users"]

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("form submitted!")
        username = request.form['username']
        password = request.form['password']


        user = user_collection.find_one({"username": username})
        if not user:
            return 'User not found. <a href="/login">Try again</a>'
        elif user['password'] == password:
            session['user'] = username
            print(f"User {username} logged in!")
            return redirect('/game')
        else: 
            return 'Invalid username or password. <a href="/login">Try again</a>'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = user_collection.find_one({"username": username})
        if existing_user:
            return "Username already exists. <a href='/'>Try again</a>"

        user_collection.insert_one({
            "username" : username,
            "password" : password
        })

        session['user'] = username
        print(f"User {username} signed up!")
        
        return redirect('/game')
    return render_template('signup.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'user' in session:
        username = session['user']
        return f"""
        <h1>Welcome to the Game, {username}!</h1>
        <p>This is your game page. (Coming soon...)</p>
        <a href="/logout">Logout</a>
        """
    else:
        return redirect('/login')
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == '__main__':
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)