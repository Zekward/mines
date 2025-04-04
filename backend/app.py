from flask import Flask, render_template, request
import webbrowser
from threading import Timer

app = Flask(__name__)
users = {}

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            return 'User not found'
        elif users[username] == password:
            return 'Login successful'
        else: 
            return 'Invalid username or password'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        
        return 'Signup successful!'
    return render_template('signup.html')

if __name__ == '__main__':
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)