from flask import Flask,render_template,request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

app = Flask(__name__,template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bullbear'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Register(db.Model): 
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique = True , index=True ,nullable = False)
    password = db.Column(db.String(500))
    confirm_pass = db.Column(db.String(500))
    
    
    def __init__(self ,email,password,username,confirm_pass):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')
        self.confirm_pass = bcrypt.hashpw(confirm_pass.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')
         
        
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8') , self.password.encode('utf-8'))
        
with app.app_context():
    db.create_all()
        


@app.route("/")

def home():
    return render_template('index.html')




@app.route("/index")

def Home():
    return render_template('index.html')





@app.route("/contact",methods = ['GET','POST'])

def contact():
    if (request.method == 'POST'):
        name =request.form.get('name')
        email =request.form.get('email')
        phone =request.form.get('phone')
        message =request.form.get('message')
        
        entry = Contacts(name=name , email=email ,date= datetime.now() ,phone_num=phone ,msg=message )
        db.session.add(entry)
        db.session.commit()        
    return render_template('contact.html')




@app.route("/about")

def About():
    return render_template('about.html')






@app.route("/news")

def post():
    return render_template('news.html')






@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Register.query.filter_by(email=email).first()
        
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['username'] = user.username
                session['email'] = user.email
                print("User authenticated successfully")
                return redirect('/dashboard')
            else:
                error = 'Invalid password'
                print("Invalid password")
        else:
            error = 'User not found'
            print("User not found")
    
    return render_template('login.html', error=error)



   



@app.route("/register", methods=['GET', 'POST'])
def Registration():
    error = None 
    if (request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password'] 
        
        existing_user = Register.query.filter_by(email=email).first()
        if existing_user:
            error = 'Email already exists. Please use a different email.'
        else:
            new_user = Register(username=username, email=email, password=password, confirm_pass=confirm_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    
    return render_template('register.html', error=error)






@app.route("/dashboard")

def Dashboard():
        if 'username' in session and  session['username']: 
            return render_template('dashboard.html')
    
        return render_template('login.html')
    





app.run(debug=True)
