from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
import db_mgmt as dbm
app = Flask(__name__) #create instance of class Flask

app.secret_key = os.urandom(32)

@app.route('/')
def root_redirect():
    print(session)
    # if logged in, go home
    if 'username' in session:
        return redirect(url_for('home'))

    # else go to login/landing page
    else:
        return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def authenticate():
    # get inputs and action type
    username = request.form['username']
    password = request.form['password']
    action = request.form['action']

    # if either is blank, redirect them back to landing
    if (username == '' or password == ''):
        flash('Invalid username or password!')
        return redirect(url_for('root_redirect'))

    # if they're trying to log in
    if (action == 'Login'):
        # stores success value of auth fxn in dbm
        success = dbm.auth_user(username, password)

        # if login successful
        if success:
            # store username in cookies and send them home
            session['username'] = username
            return redirect(url_for('home'))
        # otherwise flash them and send them back to landing
        else:
            flash('Incorrect username or password!')
            return redirect(url_for('landing'))

    # if they want to create an account
    elif (action == 'Create Account'):
        success = dbm.register(username, password)

        # if account creation successful
        if success:
            # store username in cookies and send them home
            session['username'] = username
            return redirect(url_for('home'))
        # otherwise flash them and send them back to landing
        else:
            flash('Username taken!')
            return redirect(url_for('landing'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('landing'))

# renders home
@app.route('/home')
def home():
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    return render_template('home.html', username=session['username'])

# does actions for form(s) in /home
@app.route('/home_action', methods=['POST'])
def home_action():
    # stores action user has clicked on
    action = request.form['action']

    if (action == 'Create a story'):
        return redirect(url_for('create'))

    elif (action == 'Add to a story'):
        return redirect(url_for('add'))

    elif (action == "View stories you've edited"):
        return redirect(url_for('my_stories'))

@app.route('/create', methods=["GET", "POST"])
def create():
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    return render_template('create.html')

@app.route('/create_action', methods=["POST"])
def create_action():

    # get input
    new_title = request.form['title']
    new_content = request.form['new_content']

    # check if verify title
    if ('check_title' in request.form):
        if (dbm.return_story(new_title) == None):
            flash('Story name not taken!')
        else:
            flash('Story name already taken!')
        return redirect(url_for('create'))

    # if story doesn't exist, create it
    if dbm.return_story(new_title) == None:
        dbm.create_story(new_title, new_content, session['username'])
        flash('Story creation successful!')
        return redirect(url_for('root_redirect'))
    # else flash user and send to create
    else:
        flash('Story name already taken!')
        return redirect(url_for('create'))

@app.route('/add')
def add():
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    return render_template('add.html')

@app.route('/add_action')
def add_action():
    query = request.args['query']
    print('query: {}'.format(query))
    action = request.args['submit']

    if (action == 'Random Story'):
        story = dbm.random_story()[0]
        if (story == None):
            flash('No stories in the database!')
            return redirect(url_for('add'))
        else:
            if (dbm.edited_or_not(story, session['username'])):
                return redirect(url_for('view', title=story))
            else:
                return redirect(url_for('edit', title=story))
    elif (action == 'Search'):
        return redirect(url_for('search', user_query=query))

@app.route('/search/<user_query>')
def search(user_query):
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    search_results = dbm.search_story(user_query)
    if (len(search_results) == 0):
        flash('We found no stories that match your query :(')
        return redirect(url_for('add'))
    else:
        return render_template('search.html', results=search_results, query=user_query)

@app.route('/search_action', methods=["POST"])
def search_action():
    title_clicked = request.form['result']
    if (dbm.edited_or_not(title_clicked, session['username'])):
        return redirect(url_for('view', title=title_clicked))
    else:
        return redirect(url_for('edit', title=title_clicked))

@app.route('/edit/<title>')
def edit(title):
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    story_tuple = dbm.return_story(title)
    return render_template('edit.html', title=story_tuple[0], last_content=story_tuple[2])

@app.route('/edit_action', methods=["POST"])
def edit_action():
    story_title = request.form['title']
    new_content = request.form['new_content']

    dbm.add_to_story(story_title, new_content, session['username'])

    flash('Your addition to the story was submitted!')
    return redirect(url_for('view', title=story_title))

@app.route('/my_stories')
def my_stories():
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    my_story_list = dbm.edited_stories(session['username'])
    return render_template('my_stories.html', results=my_story_list)

@app.route('/my_stories_action', methods=["POST"])
def my_stores_action():
    story_title = request.form['result']
    return redirect(url_for('view', title=story_title))

@app.route('/view/<title>')
def view(title):
    if not 'username' in session:
        flash('Please sign in or create an account first!')
        return redirect(url_for('root_redirect'))
    if not title in dbm.edited_stories(session['username']):
        flash('You can\'t access that page!')
        return redirect(url_for('root_redirect'))
    story_tuple = dbm.return_story(title)
    return render_template('view.html', title=story_tuple[0], content=story_tuple[1].split('\n'))

if __name__ == '__main__':
    app.debug = True
    app.run()
