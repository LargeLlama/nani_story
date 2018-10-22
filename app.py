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

    dbm.create_story(new_title, '', '')

    return render_template('edit.html', title=new_title, last_content="")



@app.route('/search')
def show_search():
    user_query = request.args['query']

    # search for story

    # gets tuple of story titles and redirects to search.html, which loops + displays titles as form inputs
    return render_template('search.html', results=["Jesus is my father", "Jimmy is my sister", "soojinchoi"], query=user_query)


@app.route('/edit', methods=["POST"])
def edit():
    to_edit = request.form['result']

    story_tuple = dbm.return_story(to_edit)

    return render_template('edit.html', title=story_tuple[0], last_content=story_tuple[2])

@app.route('/add_to_story', methods=["POST"])
def add_to_story():
    story_title = request.form['title']
    new_content = request.form['new_content']

    dbm.add_to_story(story_title, new_content)

    flash('Your addition to the story was submitted!')
    return redirect(url_for('view_story', title=story_title))

@app.route('/view?title=<title>')
def view_story(title):
    story_tuple = dbm.return_story(title)

    return render_template('view.html', title=story_tuple[0], content=story_tuple[1])




if __name__ == '__main__':
    app.debug = True
    app.run()
