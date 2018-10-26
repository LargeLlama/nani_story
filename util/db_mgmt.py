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

    db.commit()
    db.close()

def create_story(title, content, user):
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
        db.close()
        return False

    command_tuple = (title,content,content)
    c.execute('INSERT INTO stories VALUES(?,?,?)',command_tuple)
    command_tuple = (user,title)
    c.execute('INSERT INTO story_edits VALUES(?,?)',command_tuple)


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
            db.close()
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
        new_story = entry[1] + '\n' + content
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
    count = 0
    current_count = 0
    story = None

    # get the number of rows of the table
    c.execute('SELECT count(*) FROM stories')
    for entry in c:
        # if there's nothing in the db
        if entry[0] == 0:
            return story
        count = random.randint(0,entry[0] - 1)

    c.execute('SELECT * FROM stories')
    for entry in c:
        #print('entry: {} current_count: {}'.format(entry,current_count))
        if current_count == count:
            story = entry
            break
        current_count+=1

    return story

def edited_stories(user):
    '''
    returns a list of the titles of stories that the user has edited
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    titles = []

    command_tuple = (user,)
    c.execute('SELECT title FROM story_edits WHERE username = (?)', command_tuple)

    for entry in c:
        titles.append(entry[0])

    return titles

def edited_or_not(title, user):
    '''
    returns a boolean based on whether the user has edited or not.
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    boolean = False

    command_tuple = (title,user)
    c.execute('SELECT * FROM story_edits WHERE title = (?) AND username = (?)', command_tuple)

    for entry in c:
        boolean = True

    db.close()
    return boolean


def return_story(title):
    '''
    Return a story for viewing purposes.
    Returns None if no story with the title is found.
    Returns the tuple (title, story, last_edit) if title found.
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    return_entry = None

    command_tuple = (title,)
    c.execute('SELECT * FROM stories WHERE title = (?)', command_tuple)

    for entry in c:
        return_entry = entry

    db.close()
    return return_entry

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
        if (entry[0].lower().find(title.lower()) != -1):
            list_stories.append(entry[0])

    db.close()
    return list_stories

def main():
    create_db()
    register('user', 'password')
    register('j', 'k')
    register('Jesus', 'bread')
    print('creating help me: {}'.format(create_story("help me","peanut butter in roof of mouth help",'Jesus')))

if __name__ == '__main__':
    main()
