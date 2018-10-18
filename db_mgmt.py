import sqlite3

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


def create_story(title, content, last_edit):
    '''
    Takes the title, content, and user and adds it to the dbs
    Assumes that the user has been verified by Flask.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    command_tuple = (title, content, last_edit)
    c.execute('INSERT INTO stories VALUES(?,?,?)',command_tuple)
    c.execute('SELECT * FROM stories')

    for entry in c:
        print(entry)

    db.commit()
    db.close()

def auth_user(user):
    '''
    ensures the user is in the db.
    '''
    pass

def add_to_story(title, content):
    '''
    Finds the story that goes by title in the database
    Adds content to the end of the story and updates last_edit
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT * FROM stories')

    for entry in c:
        print(entry)
        if (entry[0] == title):
            print("Story found")
            new_story = entry[1] + content
            add_tuple = (new_story, content, title)
            c.execute('UPDATE stories SET story = (?), last_edit = (?) WHERE title = (?)', add_tuple)

    db.commit()
    db.close()

if __name__ == '__main__':
    create_db()
    create_story("soojinchoi","soojinchoi","soojinchoi")
    add_to_story("soojinchoi"," blah blah blah")
