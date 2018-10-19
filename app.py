from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
import db_mgmt as dbm
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
        success = dbm.auth_user(username, password)
        if success:
            session['username'] = username
            return render_template('home.html', username=session['username'])
        else:
            flash('Incorrect username or password!')
            return redirect(url_for('root_redirect'))

    elif (action == 'Create Account'):
        success = dbm.register(username, password)
        if success:
            session['username'] = username
            return render_template('home.html', username=session['username'])
        else:
            flash('Username taken!')
            return redirect(url_for('root_redirect'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('root_redirect'))

@app.route('/home', methods=['POST'])
def home():
    action = request.form['action']

    if (action == 'Create a story'):
        return render_template('create.html')

    elif (action == 'Add to a story'):
        return render_template('add.html')

@app.route('/create')
def create():
    new_title = request.args['title']

    # insert title into DB

    return render_template('edit.html', title=new_title, last_content="")

# @app.route('/search')
# def show_search():
#     query = request.args('query')
#
#     # search for story
#
#     # gets tuple of story titles and redirects to search.html, which loops + displays titles as form inputs
#
#





if __name__ == '__main__':
    app.debug = True
    app.run()
