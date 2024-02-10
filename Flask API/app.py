from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello wrold!!"

from controller import user_controller