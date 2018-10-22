import sqlite3
import random

DB_FILE="./data/stories.db"

def create_db():
    '''
    Creates the db.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    c.execute('CREATE TABLE user (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE story_edits (username TEXT, title TEXT)')
    c.execute('CREATE TABLE stories (title TEXT PRIMARY KEY, story TEXT, last_edit TEXT)')


def create_story(title, content):
    '''
    Takes the title, content, and user and adds it to the dbs
    Assumes that the user has been verified by Flask.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    # check if title exists
    command_tuple = (title,)
    c.execute('SELECT * FROM stories WHERE title = (?)', command_tuple)
    # if there are tuples, then the story title exists and return false
    for entry in c:
        return False

    command_tuple = (title,content,content)
    c.execute('INSERT INTO stories VALUES(?,?,?)',command_tuple)

    db.commit()
    db.close()

    return True

def register(user,password):
    '''
    register username and password.
    returns True if registered successfully.
    returns False if not.
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command_tuple = (user,)
    # check if user exists
    c.execute('SELECT * FROM user WHERE username = (?)', command_tuple)
    # if there are tuples, then the user exists and return false
    for entry in c:
        return False

    command_tuple = (user,password)
    c.execute('INSERT INTO user VALUES(?,?)',command_tuple)

    db.commit()
    db.close()
    return True

def auth_user(user, password):
    '''
    ensures the user is in the db upon login submission.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    command_tuple = (user,password)
    c.execute('SELECT * FROM user WHERE username = (?) AND password = (?)', command_tuple)

    for entry in c:
        # check auth
        if entry[0] == user and entry[1] == password:
            return True

    db.close()
    # return false at end
    return False

def add_to_story(title, content, user):
    '''
    Finds the story that goes by title in the database
    Adds content to the end of the story and updates last_edit
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    select_tuple = (title,)
    c.execute('SELECT * FROM stories WHERE title = (?)', select_tuple)

    for entry in c:
        new_story = entry[1] + "\n" + content
        add_tuple = (new_story, content, title)
        c.execute('UPDATE stories SET story = (?), last_edit = (?) WHERE title = (?)', add_tuple)
        user_tuple = (user, title)
        c.execute('INSERT INTO story_edits VALUES(?,?)', user_tuple)

    db.commit()
    db.close()

def random_story():
    '''
    Return a randomly selected story.
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

def edited_stories(user):
    '''
    returns a list of the titles of stories that the user has edited
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    titles = []

    command_tuple = (user,)
    c.execute('SELECT * FROM story_edits WHERE username = (?)', command_tuple)

    for entry in c:
        titles.append(entry)

    return titles

def return_story(title):
    '''
    Return a story for viewing purposes.
    Returns None if no story with the title is found.
    Returns the tuple (title, story, last_edit) if title found.
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command_tuple = (title,)
    c.execute('SELECT * FROM stories WHERE title = (?)', command_tuple)

    for entry in c:
        return entry
    db.close()

def search_story(title):
    '''
    Return a list of stories that you searched for
    returns a list of the titles of all the stories found
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    list_stories = []

    c.execute('SELECT title FROM stories')

    for entry in c:
        if (entry[0].find(title) != -1):
            list_stories.append(entry[0])

    db.close()
    return list_stories


if __name__ == '__main__':
    #create_db()
    print('creating soojinchoi: {}'.format(create_story("soojinchoi","soojinchoi")))
    print('creating soojin2: {}'.format(create_story("soojin2","story time")))
    print('creating soojin3: {}'.format(create_story("soojin3","adios amigos")))
    add_to_story("soojinchoi"," blah blah blah", "j")
    print('registering j: {}'.format(register('j', 'k')))
    print('authenticating soojin: {}'.format(auth_user('soojinchoi', 'soojinchoi')))
    print('authenticating j: {}'.format(auth_user('j', 'k')))
    print('return_story: {}'.format(return_story('soojinchoi')))
    print('returning a sample search: {}'.format(search_story('soojin')))
    print('returning all stories edited by j:{}'.format(edited_stories('j')))
