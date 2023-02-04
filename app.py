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

# app name
@app.errorhandler(404)
  
# inbuilt function which takes error as parameter
def not_found(e):
  
# defining function
  return render_template("404.html")


ds = []    
@app.route('/',methods=["GET"])
def index(): 
    if session.get('lange') == None or session.get('lange') != "":
        session['lang'] = "th"
    prodcut_type = func.product_type.all_type()
    
    return render_template('index.html',data = prodcut_type,lange = session['lang'],ds=ds)


@app.route('/lang/<lang>',methods=["GET"])
def lange(lang):
    session['lang'] = lang
    return redirect(url_for('index'))

@app.route('/category/<productname>/<int:type>',methods=["GET"])
def category(productname,type): 
    prodcut_type = productname
    uid = type
    data = func.product_type.product_byTypeId(uid)
    return render_template('product.html',productname = prodcut_type,data=data,uid=uid ,ds=ds)    

@app.route('/addcart',methods=['POST','GET','DELETE'])
def addcart():
    if request.method == "POST":
        ds = session.get('ds')
        if ds == None:
            ds =[]
        if session.get('username') != None  :
            data = request.form
            pname = data['pname']
            puid = data['pid']
            pimg = data['pimg']
            pprice= data['pprice']
            pqauntity = data['pqauntity']
            punit = data['punit']
            for i in range(len(ds)):
                if ds[i]['puid'] == puid:
                    ds[i]['qauntity'] += int(pqauntity) 
                    session['ds'] = ds
                    return  redirect(url_for('addcart')) 
            ds.append({'pname':pname,'puid':puid,'pimg':pimg,'pprice':pprice ,'punit':punit,'qauntity':int(pqauntity)})
            session['ds'] = ds
            return redirect(url_for('addcart'))
        return redirect(url_for('login'))
    elif request.method == "GET":
        ttotal = session.get('ds')
        count = len(ttotal)
        t = 0
        q = 0
        for item in ttotal:
            t+=float(item['pprice']) * int(item['qauntity'])
            q+=int(item['qauntity'])
        return render_template('product_cart.html',ds=session.get('ds'),count = count,t=t ,q=q)



@app.route('/del_cart', methods=['POST','GET'])
def del_cart():
    if request.method == "POST":
        data = request.form
        puid = data['puid']
        dd = session.get('ds')
        if dd != None:
            for i in range(len(dd)):
                if dd[i]['puid'] == puid:
                    del dd[i]
                    session['ds'] = dd
                    return  redirect(url_for('addcart')) 
        return  redirect(url_for('addcart')) 
    else:
        return redirect(url_for('addcart'))

@app.route('/minute/<puid>', methods=['GET'])
def minute(puid):
    if request.method == "GET":
        dd = session.get('ds')
        if dd != None:
            for i in range(len(dd)):
                if dd[i]['puid'] == puid :
                    dd[i]['qauntity'] -=1 
                    session['ds'] = dd
                    if dd[i]['qauntity'] == 0:
                        del dd[i]
                        session['ds'] = dd
                        return  redirect(url_for('addcart')) 

                    return  redirect(url_for('addcart')) 
            return  redirect(url_for('addcart')) 

@app.route('/plus/<puid>', methods=['GET'])
def plus(puid):
    if request.method == "GET":
        dd = session.get('ds')
        if dd != None:
            for i in range(len(dd)):
                if dd[i]['puid'] == puid:
                    
                    dd[i]['qauntity'] +=1 
                    session['ds'] = dd
                    return  redirect(url_for('addcart')) 
        return  redirect(url_for('addcart'))



@app.route('/billpayment',methods=['POST'])
def billpayment():
    data = request.form
    paymentdata = data['obj']
    return jsonify(paymentdata)




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
    return render_template('auth/login.html',massage ="email or password is valid!!")


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