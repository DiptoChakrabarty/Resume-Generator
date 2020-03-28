from flask import Flask,render_template,url_for,flash,redirect,request,abort
from resume.forms import Reg,Login,account,posting,resumebuilder
from resume.models import user,posts,education,experience,projects
from resume import app,db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os
from PIL import Image

title = "Posts"

@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/Posts")
def about():
    pos = posts.query.all()
    return  render_template("about.html",posts=pos, title=title)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = Reg()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = user(username=form.username.data,email=form.email.data,password=hashed)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = Login()
    if form.validate_on_submit():
        logged = user.query.filter_by(email=form.email.data).first()
        if logged and bcrypt.check_password_hash(logged.password,form.password.data):
            login_user(logged,remember=form.remember.data)
            next_page = request.args.get('next')            
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('hello'))
        else:
            flash('Login unsuccessful')

    return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("hello"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(form_picture.filename)
    pic = random_hex + ext
    path = os.path.join(app.root_path,'static/profiles',pic)
    
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(path)

    return pic



@app.route("/accounts",methods=['GET','POST'])
@login_required          #checks if user logged in or not and then allows access
def accounts():
    form= account()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.picture = pic_file
        current_user.username = form.new_username.data
        current_user.email = form.new_email.data  # Update current user values
        db.session.commit()
        flash("Your Account has been updated","success")
        return redirect(url_for("accounts"))
    elif request.method == 'GET':
        form.new_username.data = current_user.username
        form.new_email.data = current_user.email
    image_file = url_for('static',filename='profiles/'+ current_user.image_file)
    return render_template("account.html",title="Account",image_file=image_file,form=form)


@app.route("/posts/new",methods=['GET','POST'])
@login_required
def  post():
    form = resumebuilder()
    if form.validate_on_submit():
        edu = education(name=form.college.data,start=form.start.data,end=form.end.data,cgpa=form.cgpa.data,edu=current_user)
        print(form.college.data,form.start.data,form.end.data)
        db.session.add(edu)
        db.session.commit()
        print(form.company.data,form.position.data)
        
        exp = experience(company=form.company.data,position=form.position.data,startexp=form.startexp.data,endexp=form.endexp.data,content=form.content.data,exp=current_user)
        db.session.add(exp)
        db.session.commit()

        pro = projects(projectname=form.projectname.data,startpro=form.startpro.data,endpro=form.endpro.data,description=form.description.data,url=form.url.data)
        db.session.add(pro)
        db.session.commit()

        return redirect(url_for("hello"))
    return render_template("posts.html",title="New Posts",form=form)





     







