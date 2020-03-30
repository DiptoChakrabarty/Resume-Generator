from flask import Flask,make_response,render_template,url_for,flash,redirect,request,abort
from resume.forms import Reg,Login,account,posting,resumebuilder,useredu,userexp,userpro,usersk,achieve
from resume.models import user,posts,education,experience,projects,userdetails,skills,achievements
from resume import app,db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os
from PIL import Image
import pdfkit

title = "Posts"

@app.route("/")
def hello():
    return render_template("home.html")




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


@app.route("/resume/new",methods=['GET','POST'])
@login_required
def  post():
    form = resumebuilder()
    if form.validate_on_submit():
        usr = userdetails(name=form.name.data,email=form.email.data,designation=form.designation.data,phoneno=form.phoneno.data,profile=form.profile.data,details=current_user)
        db.session.add(usr)
        db.session.commit()
        print(form.name.data,form.email.data,form.designation.data)
        return redirect(url_for("postedu"))
    return render_template("posts.html",title="New Resume",form=form)

#### Separation#####
@app.route("/resume/new/education",methods=['GET','POST'])
@login_required
def  postedu():
    form = useredu()
    eduadded = education.query.filter_by(edu=current_user).all()
    if form.validate_on_submit():
        edu = education(name=form.college.data,start=form.start.data,end=form.end.data,cgpa=form.cgpa.data,edu=current_user)
        print(form.college.data,form.start.data,form.end.data)
        db.session.add(edu)
        db.session.commit()
        #print(form.company.data,form.position.data)
        return redirect(url_for("postedu"))
    return render_template("education.html",title="Education",form=form,eduadded=eduadded)


@app.route("/resume/new/experience",methods=['GET','POST'])
@login_required
def  postexperience():
    form = userexp()
    expadded = experience.query.filter_by(exp=current_user).all()
    if form.validate_on_submit():
        exp = experience(company=form.company.data,position=form.position.data,startexp=form.startexp.data,endexp=form.endexp.data,content=form.content.data,exp=current_user)
        db.session.add(exp)
        db.session.commit()
        return redirect(url_for("postexperience"))
    return render_template("experience.html",title="Experience",form=form,expadded=expadded)


@app.route("/resume/new/projects",methods=['GET','POST'])
@login_required
def  postprojects():
    form = userpro()
    proadded = projects.query.filter_by(pro=current_user).all()
    if form.validate_on_submit():
        pro = projects(projectname=form.projectname.data,startpro=form.startpro.data,endpro=form.endpro.data,description=form.description.data,url=form.url.data,pro=current_user)
        db.session.add(pro)
        db.session.commit()
        return redirect(url_for("postprojects"))
    return render_template("projects.html",title="Projects",form=form,proadded=proadded)

@app.route("/resume/new/skills",methods=['GET','POST'])
@login_required
def postskills():
    form = usersk()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    if form.validate_on_submit():
        sk = skills(skillname=form.skillname.data,skill=current_user)
        db.session.add(sk)
        db.session.commit()
        return redirect(url_for("postskills"))
        #print(form.skillname.data)

    return render_template("skills.html",title="Skills",form=form,skillsadded=skillsadded)


@app.route("/resume/new/acheive",methods=['GET','POST'])
@login_required
def postacheive():
    form = achieve()
    achadded = achievements.query.filter_by(ach=current_user).all()
    if form.validate_on_submit():
        acheive = achievements(achname=form.achname.data,achdesc=form.achname.data,ach=current_user)
        db.session.add(acheive)
        db.session.commit()
        return redirect(url_for("postskills"))
        #print(form.skillname.data)

    return render_template("acheive.html",title="Acheivements",form=form,achadded=achadded)
       
       


#### End Separation ####




### Generate Resume


@app.route("/resume",methods=["GET","POST"])
@login_required
def resumeview():
    edu = education.query.filter_by(edu=current_user).all()
    exp = experience.query.filter_by(exp=current_user).all()
    pro = projects.query.filter_by(pro=current_user).all()
    usr = userdetails.query.filter_by(details=current_user).first()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    achmade = achievements.query.filter_by(ach=current_user).all()
    

    image_file = url_for('static',filename='profiles/'+ current_user.image_file)

    return render_template("resume.html",edu=edu,exp=exp,pro=pro,usr=usr,sk=skillsadded,achmade=achmade,image_file=image_file)




@app.route("/download",methods=["GET"])
@login_required
def downloadpdf():
    edu = education.query.filter_by(edu=current_user).all()
    exp = experience.query.filter_by(exp=current_user).all()
    pro = projects.query.filter_by(pro=current_user).all()
    usr = userdetails.query.filter_by(details=current_user).first()
    skillsadded = skills.query.filter_by(skill=current_user).all()
    achmade = achievements.query.filter_by(ach=current_user).all()

    image_file = url_for('static',filename='profiles/'+ current_user.image_file)
    css = ["resume/static/resume.css","resume/static/main.css"]
    rendered = render_template("resume.html",edu=edu,exp=exp,pro=pro,usr=usr,sk=skillsadded,achmade=achmade,image_file=image_file)
    pdf =pdfkit.from_string(rendered,False,css=css)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachement; filename=resume.pdf"

    return response
    



### Updating and deleting
#acheivments
@app.route("/resume/new/acheive/<int:acheive_id>/update",methods=["GET","POST"])
def update_acheive(acheive_id):
    achview = achievements.query.get_or_404(acheive_id)

    form = achieve()
    if form.validate_on_submit():
        achview.achname = form.achname.data
        achview.achdesc = form.achdesc.data
        db.session.commit()
        flash('Your acheivement has been updated!', 'success')
        return redirect(url_for('postacheive'))
    elif request.method == 'GET':
        form.achname.data= achview.achname
        form.achdesc.data = achview.achdesc
    return render_template("acheive.html",title="Update Acheivement",form=form)

@app.route("/resume/new/acheive/<int:acheive_id>/delete",methods=["GET","POST"])
def delete_acheive(acheive_id):
    achview = achievements.query.get_or_404(acheive_id)

    db.session.delete(achview)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('postacheive'))

#education
@app.route("/resume/new/education/<int:education_id>/update",methods=["GET","POST"])
def update_edu(education_id):
    eduview = education.query.get_or_404(education_id)

    form = useredu()
    if form.validate_on_submit():
        eduview.name = form.college.data
        eduview.start = form.start.data
        eduview.end = form.end.data
        eduview.cgpa = form.cgpa.data
        db.session.commit()
        flash('Your education details have been updated!', 'success')
        return redirect(url_for('postedu'))
    elif request.method == 'GET':
        form.college.data= eduview.name
        form.start.data = eduview.start
        form.end.data = eduview.end
        form.cgpa.data =  eduview.cgpa
    return render_template("education.html",title="Update Education",form=form)

@app.route("/resume/new/education/<int:education_id>/delete",methods=["GET","POST"])
def delete_edu(acheive_id):
    eduview = education.query.get_or_404(education_id)

    db.session.delete(eduview)
    db.session.commit()
    flash('Your education detail post has been deleted!', 'success')
    return redirect(url_for('postedu'))


#Experience
@app.route("/resume/new/experience/<int:experience_id>/update",methods=["GET","POST"])
def update_exp(experience_id):
    expview = experience.query.get_or_404(experience_id)

    form = userexp()
    if form.validate_on_submit():
        expview.company = form.company.data
        expview.startexp = form.startexp.data
        expview.endexp = form.endexp.data
        expview.content = form.content.data
        db.session.commit()
        flash('Your education details have been updated!', 'success')
        return redirect(url_for('postexperience'))
    elif request.method == 'GET':
        form.company.data= expview.company
        form.startexp.data = expview.startexp
        form.endexp.data = expview.endexp
        form.content.data =  expview.content
    return render_template("experience.html",title="Update Work Experience",form=form)

@app.route("/resume/new/experience/<int:experience_id>/delete",methods=["GET","POST"])
def delete_exp(experience_id):
    expview = experience.query.get_or_404(experience_id)

    db.session.delete(expview)
    db.session.commit()
    flash('Your experience detail post has been deleted!', 'success')
    return redirect(url_for('postexp'))
    

#Projects
@app.route("/resume/new/projects/<int:project_id>/update",methods=["GET","POST"])
def update_pro(project_id):
    proview = projects.query.get_or_404(project_id)

    form = userpro()
    if form.validate_on_submit():
        proview.projectname = form.projectname.data
        proview.startpro = form.startpro.data
        proview.endpro = form.endpro.data
        proview.description = form.description.data
        proview.url  = form.url.data
        db.session.commit()
        flash('Your project details have been updated!', 'success')
        return redirect(url_for('postprojects'))
    elif request.method == 'GET':
        form.projectname.data= proview.projectname
        form.startpro.data = proview.startpro
        form.endpro.data =  proview.endpro
        form.description.data =  proview.description
        form.url.data = proview.url
    return render_template("projects.html",title="Update Projects",form=form)

@app.route("/resume/new/projects/<int:project_id>/delete",methods=["GET","POST"])
def delete_pro(project_id):
    proview = projects.query.get_or_404(project_id)

    db.session.delete(proview)
    db.session.commit()
    flash('Your project detail post has been deleted!', 'success')
    return redirect(url_for('postprojects'))
    
   

    







     







