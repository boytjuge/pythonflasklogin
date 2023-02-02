from flask import Flask, jsonify , redirect, render_template , url_for, session,request
from flask_cors import CORS
from function.func import *
app = Flask(__name__)
app.secret_key = "@38d8@884*$*8428fdsdf__0fs99"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)


@app.route("/api/v1/users",methods=['GET'])
def list_users():
    data = fn([{'username':'admin'},{'username':'local'}])
    return jsonify(data)




@app.route('/',methods=["GET"])
def index():
    if session.get('username') == None  :
        return redirect(url_for('login')) 
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return  render_template('auth/login.html')
    elif request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('index'))


@app.route('/register')
def register():
    return  render_template('auth/register.html')

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username', default=None)
    return  redirect(url_for('login'))

if __name__  == "__main__":
    app.run(debug=True,host='127.0.0.1',port=5000)