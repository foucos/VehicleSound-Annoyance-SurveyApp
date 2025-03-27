from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from models.user import user
import time

app = Flask(__name__,static_url_path='')

app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return 'Homepage'

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))
   
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'), request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)

#logout endpoint
@app.route('/logout',methods=['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')
    
#endpoint route for static files    
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/main')
def main():
    if checkSession() == False:
        return redirect('/login')
    return render_template('main.html', title='Main menu')
    
#standalone function to be called when we need to cjeck if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False
        
'''        
@app.route('/main')
def main():
    if checkSession() == False:
       return redirect('/login')
    return render_template('main.html', title='Main menu')
   
    if checkSession() == False:
        return redirect('/login')
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu')
    else:
        return render_template('customer_main.html', title='Main menu')
'''



if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   