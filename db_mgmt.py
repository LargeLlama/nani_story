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


def create_story(title, content, user):
    '''
    Takes the title, content, and user and adds it to the dbs
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    c.execute('SELECT {} FROM user'.format(user))

     

if __name__ == '__main__':
    #create_db()
