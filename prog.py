from typing import Collection
from flask import Flask, render_template, url_for, request, redirect, session, flash
import flask_login

from flask_login import LoginManager, login_user


#from flask_login import login_manager, login_required, logout_user

from flask_login import login_user, login_required, logout_user

import bcrypt
import pymongo

from pymongo import MongoClient
from pymongo import collection


app = Flask(__name__)
app.secret_key="cheie secreta"

parola = ""

cluster=MongoClient("mongodb+srv://bianca:orsova2021@cluster0.cqjml.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["baze"]


@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
    else:
        user = 'Vizitator'
    return render_template('/index.html', user=user)


@app.route('/torturi')
def pagina_torturi():
    if 'username' in session:
        user = session['username']
    else:
        user = 'Vizitator'

    collection=db["torturi"]
    items=[
        {'id':1,'nume':'Tort Choco-Mint','cod_bara':'123456789','pret':110,'poza':'static/torturi/choco.jpeg'}, 
        {'id':2,'nume':'Tort Ferrero Rocher','cod_bara':'123456789','pret':130,'poza':'static/torturi/ferero.jpeg'}, 
        {'id':3,'nume':'Tort Pavlova','cod_bara':'123456789','pret':120,'poza':'static/torturi/pavlova.jpeg'}, 
        {'id':4,'nume':'Tort Tropical mango & cocos','cod_bara':'123456789','pret':110,'poza':'static/torturi/tiramisu.jpeg'}, 
        {'id':5,'nume':'Tort Medovik','cod_bara':'123456789','pret':130,'poza':'static/torturi/medovik.jpeg'}, 
        {'id':6,'nume':'Tort Snichers','cod_bara':'123456789','pret':130,'poza':'static/torturi/snickers.jpeg'}, 
        {'id':7,'nume':'Tortul cifra ','cod_bara':'123456789','pret':130,'poza':'static/torturi/cifra.jpg'}, 
        {'id':8,'nume':'Tortul Choco-Berry','cod_bara':'123456789','pret':110,'poza':'static/torturi/choco.jpeg'},
        {'id':9,'nume':'Tortul Carrot Cake','cod_bara':'123456789','pret':110,'poza':'static/torturi/morcovi.jpeg'}, 
        {'id':10,'nume':'Tortul Black Forest','cod_bara':'123456789','pret':110,'poza':'static/torturi/tropical.jpeg'},
        {'id':11,'nume':'Tortul Amandina','cod_bara':'123456789','pret':110,'poza':'static/torturi/amandina.jpeg'}, 
        {'id':12,'nume':'Tortul Diplomat','cod_bara':'123456789','pret':110,'poza':'static/torturi/diplomat.jpeg'}, 
        {'id':13,'nume':'Tortul Tiramisu','cod_bara':'123456789','pret':110,'poza':'static/torturi/tiramisu.jpeg'}, 
    ]

    for i in items:
        collection.insert_one(i)
    return render_template('/torturi.html',items=items, user=user) 

@app.route('/prajituri')
def pagina_prajituri():
    if 'username' in session:
        user = session['username']
    else:
        user = 'Vizitator'

    collection=db["prajituri"]
    items=[
        {'id':1,'nume':'Mini cannoli siciliani','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p1.jpeg'},
        {'id':2,'nume':'Mini Pavlova cu ciocolata sau vanilie','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p2.jpeg'},
        {'id':3,'nume':'Mini tarte cu ciocolata sau vanilie','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p3.jpg'},
        {'id':4,'nume':'Cheesecake','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p4.jpeg'},
        {'id':5,'nume':'Briose ( cupcakes )','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p5.jpeg'},
        {'id':6,'nume':'Brownie cu ciocolata','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p6.jpeg'},
        {'id':7,'nume':'Ciocolata de casa','cod_bara':'123456789','pret':1234,'poza':'static/prajituri/p7.jpeg'}
    ]
    for i in items:
        collection.insert_one(i)
    return render_template('/prajituri.html', items=items, user=user) 


@app.route('/candy')
def pagina_candybar():
    if 'username' in session:
        user = session['username']
    else:
        user = 'Vizitator'

    collection=db["candybar"]
    items=[
        {'id':1,'nume':'Pachet Sweet Dreams','cod_bara':'123456789','pret':1234,'poza':'static/candy/c1.jpeg'},
        {'id':2,'nume':'Candy Bar Sweet Corner ','cod_bara':'123456789','pret':1234,'poza':'static/candy/c2.jpeg'},
        {'id':3,'nume':'Candy Bar Blue Air','cod_bara':'123456789','pret':1234,'poza':'static/candy/c3.jpeg'},
        {'id':4,'nume':'Candy Bar Innedit','cod_bara':'123456789','pret':1234,'poza':'static/candy/c4.jpg'}        
    ]
    for i in items:
        collection.insert_one(i)
    return render_template('/candy.html', items=items, user=user) 

@app.route('/contact')
def pagina_contact():
    if 'username' in session:
        user = session['username']
    else:
        user = 'Vizitator'

    return render_template('/contact.html', user=user) 


@app.route('/profil')
def pagina_profil():
    global parola
    if 'username' in session:
        user = session['username']
        parola = session['password']
        return render_template('/profil.html', user=user, parola=parola) 
    else:
        user = 'Vizitator'
        parola =""
    return render_template('/index.html', user=user)

@app.route('/logout')
def logout():
    user = 'Vizitator'
    parola = ""
    flash("Ai ales operatia de iesire din aplicatie ", category='info')    
    return redirect(url_for('index'))


@app.route('/login')
def login():
    return render_template('/login1.html')

@app.route('/login1', methods=['POST'])
def login1():
    collection = db["user"]
    login_user1 = collection.find_one({'name':request.form['username']})
    print('Login user = ', login_user1)
    if login_user1:
        current_user = login_user1['name']
        parola = request.form['pass']
        hash_passwd_form = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), hash_passwd_form):
            session['username']=request.form['username']
            session['password'] = request.form['pass']
            session['intrare']=True
            
            return redirect(url_for('index'))
    
    return "Combinatie invalida utilizator / parola "


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        collection = db["user"]
        gasit_user = collection.find_one({'name':request.form['username']})
        if gasit_user is None:
            parola_hash = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            collection._insert({'name':request.form['username'],'password':parola_hash})
            session['username']=request.form['username']
            session['password'] = request.form['pass']
            return redirect(url_for('index'))
        return "Utilizatorul exista deja in baza "
    return render_template("/register.html")

if __name__=="__main__":
    app.run()
