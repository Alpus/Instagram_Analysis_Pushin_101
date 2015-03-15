from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

    
@app.route('/<username>')
def show_user_profile(username):
    return render_template('base.html', username=username)

if __name__ == "__main__":
    app.run()
