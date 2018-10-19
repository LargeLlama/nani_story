from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
app = Flask(__name__) #create instance of class Flask

app.secret_key = os.urandom(32)

@app.route('/')
def root_redirect():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('landing.html')

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    action = request.form['action']

    if (action == 'Login'):

        session['username'] = username

        return render_template('home.html', username=session['username'])

    elif (action == 'Create Account'):

        #create Account

        session['username'] = username

        return render_template('home.html', username=session['username'])

@app.route('/home')
def home():
    


if __name__ == '__main__':
    app.debug = True
    app.run()
