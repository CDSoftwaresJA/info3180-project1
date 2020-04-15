from flask import Flask, render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from forms import EmailPasswordForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'some$3cretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://icmwuvgxqphskl:29518807a50b98eff4637464f45393efd41a9e80b3dff925af7c55e28e967b28@ec2-54-210-128-153.compute-1.amazonaws.com:5432/d9u7e52sn8k5ti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "/uploads"

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    email = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    #created_on = db.Column(db.DateTime, server_default=db.func.now())
    
    def __init__(self, id,fname, lname,gender,email,biography,picture):
        self.fname=fname
        self.lname=lname
        self.gender=gender
        self.email=email
        self.biography=biography
        self.picture=picture
        def __repr__(self):
            return self.fname
db.create_all()
def toJson(user):
    dataDict = {
            'id': 'user.id',
            'fname': user.fname,
            'lname': user.lname,
            'gender': user.gender,
            'email': user.email,
            'biography': user.biography,
            'picture': user.picture

            }
    return dataDict


@app.route('/add', methods=['POST','GET']) 
def profile_add():
    form = EmailPasswordForm(request.form)
    if request.method == 'POST':
        picture=form.picture.data
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture))
        data=User(1,form.fname.data,form.lname.data,form.gender.data,form.email.data,form.biography.data,"Test")
        db.session.add(data)
        db.session.flush()
        db.session.commit()
        db.session.query(User).all()
        return jsonify(toJson(data));
    if request.method == 'GET':
        return render_template("addUser.html",form=form)
    return "Form not validated"    
    

@app.route('/', methods=['GET']) 
def home():
    return render_template("base.html")
  
@app.route('/profile/<string:id>') 
def profile_view(id):
    user = User.query.get(id)
    #return  jsonify(toJson(user))
    return render_template("viewProfile.html",user=user)
    
@app.route('/profiles/') 
def profiles():
    users = User.query.all()
    dataJson = []
    for user in users:
        dataJson.append(toJson(user))
    #return jsonify(dataJson)
    return render_template("viewProfiles.html",users=users)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
