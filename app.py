from flask import Flask, render_template, request, session, url_for, redirect, flash
import os
app = Flask(__name__) #create instance of class Flask

app.secret_key = os.urandom(32)
