from flask import Flask, jsonify , redirect, render_template , url_for, session,request
from flask_cors import CORS
from function import func 
app = Flask(__name__)
app.secret_key = "@38d8@884*$*8428fdsdf__0fs99"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)


@app.route("/api/v1/users",methods=['GET'])
def list_users():
    data = [{'username':'admin'},{'username':'local'}]
    return jsonify(data)




@app.route('/',methods=["GET"])
def index():
    if session.get('username') == None  :
        return redirect(url_for('login')) 
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        session.pop('error', default=None)
        if session.get('username') != None  :
            return redirect(url_for('index'))
        return  render_template('auth/login.html',massage=None)
    elif request.method == "POST":
        data= request.form
        if func.login.check_user(data) > 0:
            session['username']  = request.form['username']
            return redirect(url_for('index',massage=None))
        return render_template('auth/login.html',massage ="email or password is valid!!")# redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "GET":
        if session.get('username') != None  :
            return redirect(url_for('index'))    
        return  render_template('auth/register.html')
    elif request.method == "POST":
        data = request.form
        if func.register.select_user(data) == 0:
            r = func.register.insert_user(data)
            session['error'] = {"error":"success","color":"green"}
            return redirect(request.referrer)
        session['error'] = {"error":"valid","color":"red"}
        return redirect(request.referrer)


@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username',default=None)
    return  redirect(url_for('login'))

if __name__  == "__main__":
    app.run(debug=True,host='127.0.0.1',port=5000)