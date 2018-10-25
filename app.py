from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
import db_mgmt as dbm
app = Flask(__name__) #create instance of class Flask

app.secret_key = os.urandom(32)

@app.route('/')
def root_redirect():
    '''
    redirects user to appropriate page depending on whether or not they're logged in
    '''
    print(session)
    # if logged in, go home
    if 'username' in session:
        return redirect(url_for('home'))

    # else go to login/landing page
    else:
        return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    '''
    renders landing.html, the login/create-account page
    '''
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def authenticate():
    '''
    checks user credentials
    logs user in and redirects to home page if username-password pair is correct
    else flashes user and redirects back to landing
    '''
    # get inputs and action type
    username = request.form['username']
    password = request.form['password']
    action = request.form['action']

    # if either input is blank, redirect them back to landing
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
    '''
    if user is logged in, pops username from cookies
    regardless, redirects to landing page
    '''
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('landing'))

# renders home
@app.route('/home')
def home():
    '''
    renders home page with the username in session
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    return render_template('home.html', username=session['username'])

# does actions for form(s) in /home
@app.route('/home_action', methods=['POST'])
def home_action():
    '''
    takes user input from home page and...
    - redirects to create story page
    - redirects to add to story page
    - redirects to view my stories page
    depending on input
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    # stores action user has clicked on
    action = request.form['action']

    if (action == 'Create a story'):
        return redirect(url_for('create', title="None"))

    elif (action == 'Add to a story'):
        return redirect(url_for('add'))

    elif (action == "View stories you've edited"):
        return redirect(url_for('my_stories'))

# uses dynamic routing so we don't have to generate a new route for every possible title
@app.route('/create/<title>')
def create(title):
    '''
    renders create story page
    takes title as input, which is useful when checking if title is valid
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    print('title user has input\'d: {}'.format(title))
    if (title == 'None'):
        print('TITLE IS BLANK')
        title = ''
    else:
        print('TITLE IS {}'.format(title))
    return render_template('create.html', title=title)

@app.route('/create_action', methods=["POST"])
def create_action():
    '''
    takes user input from create story page and...
    - checks title then redirects back to create story page
    - creates story given title and content
    depending on input
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    # get input
    new_title = request.form['title']
    new_content = request.form['new_content']

    if (new_title == '' or new_title.strip() == ''):
        flash('Invalid title!')
        return redirect(url_for('create', title='None'))

    # check if verify title
    if ('check_title' in request.form):
        if (dbm.return_story(new_title) == None):
            flash(' &#2705;')
        else:
            flash('Story name already taken!')
        return redirect(url_for('create', title=new_title))

    # if story doesn't exist...
    if dbm.return_story(new_title) == None:
        # if new_content is blank
        if (new_content == ''):
            flash('Can\'t leave content blank!')
            return redirect(url_for('create', title=new_title))

        # if new_content only has spaces, \n, etc.
        if (new_content.strip() == ''):
            flash('Can\'t populate content with blanks!')
            return redirect(url_for('create', title=new_title))

        # else create story
        dbm.create_story(new_title, new_content, session['username'])
        flash('Story creation successful!')
        return redirect(url_for('home'))

    # else flash user and send to create
    else:
        flash('Story name already taken!')
        return redirect(url_for('create'), title='None')

@app.route('/add')
def add():
    '''
    renders add to story page
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    return render_template('add.html')

@app.route('/add_action')
def add_action():
    '''
    takes user input from add to story page and...
    - redirects to a random story
        - if the user has contributed to the chosen story, they go to the view page
        - else they go to the edit page
    - redirects to search page with the user query, which then displays search results
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
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
    '''
    searches for story based on query
    if query isn't found, flashes message and redirects user to add to story page
    else populates search page with search results
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    search_results = dbm.search_story(user_query)
    if (len(search_results) == 0):
        flash('We found no stories that match your query :(')
        return redirect(url_for('add'))
    else:
        return render_template('search.html', results=search_results, query=user_query)

@app.route('/search_action', methods=["POST"])
def search_action():
    '''
    takes user input from search page and:
    - views clicked story if user has contributed
    - otherwise, redirects user to edit page for the story
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    title_clicked = request.form['result']
    if (dbm.edited_or_not(title_clicked, session['username'])):
        return redirect(url_for('view', title=title_clicked))
    else:
        return redirect(url_for('edit', title=title_clicked))

@app.route('/edit/<title>')
def edit(title):
    '''
    renders edit page with last_edit and title of story
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    story_tuple = dbm.return_story(title)
    return render_template('edit.html', title=story_tuple[0], last_content=story_tuple[2])

@app.route('/edit_action', methods=["POST"])
def edit_action():
    '''
    takes user input from edit page and...
    - adds new content to story
    then redirects to the view page for the story
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    story_title = request.form['title']
    new_content = request.form['new_content']

    dbm.add_to_story(story_title, new_content, session['username'])

    flash('Your addition to the story was submitted!')
    return redirect(url_for('view', title=story_title))

@app.route('/my_stories')
def my_stories():
    '''
    renders a list of stories the user has contributed to in my_stories page
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    my_story_list = dbm.edited_stories(session['username'])
    return render_template('my_stories.html', results=my_story_list)

@app.route('/my_stories_action', methods=["POST"])
def my_stories_action():
    '''
    redirects user to appropriate story page when they click on a story in
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    story_title = request.form['result']
    return redirect(url_for('view', title=story_title))

# uses dynamic routing so we don't have to generate a new route for every possible title
@app.route('/view/<title>')
def view(title):
    '''
    displays story given a title
    '''
    if not 'username' in session:
        return kick_out_user_not_signed_in()
    if not title in dbm.edited_stories(session['username']):
        flash('You can\'t access that page!')

    story_tuple = dbm.return_story(title)
    return render_template('view.html', title=story_tuple[0], content=story_tuple[1].split('\n'))

def kick_out_user_not_signed_in():
    '''
    kicks out users if they're not logged in
    '''
    flash('Please sign in or create an account first!')
    return redirect(url_for('root_redirect'))

if __name__ == '__main__':
    app.debug = True
    app.run()
