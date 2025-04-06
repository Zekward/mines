from flask import Flask, render_template, request, redirect, url_for, session
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'b9f8a5c42b2f4a829bb6e7f4ef9d1b90'
users = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            return 'User not found'
        elif users[username] == password:
            session['user'] = username
            print(f"User {username} logged in!")
            return redirect('/game')
        else: 
            return 'Invalid username or password. <a href='/'>Try again</a>'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "Username already exists. <a href='/'>Try again</a>"

        users[username] = password
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