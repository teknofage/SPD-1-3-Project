from flask import render_template, send_from_directory, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, DeedForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Deed
from werkzeug.urls import url_parse
from datetime import datetime
import os


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    deeds = Deed.query.order_by(Deed.timestamp.desc()).all()
    return render_template('index.html', title='Home', deeds=deeds)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = DeedForm()
    if form.validate_on_submit():
        deed = Deed(title=form.title.data,
                    body=form.body.data, author=current_user)
        db.session.add(deed)
        db.session.commit()
        flash('Your deed is now live!')
        return redirect(url_for('user', username=current_user.username))
    deeds = Deed.query.order_by(Deed.timestamp.desc()).all()
    return render_template('user.html', user=user, form=form, deeds=deeds)


@app.route('/user/company')
@login_required
def company():
    # params for this will be "roles" roles(flask_login) = company(deedle_groups)

    deeds = Deed.query.order_by(Deed.timestamp.desc()).all()
    # set company = to comapny
    return render_template('group.html', deeds=deeds)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.group)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.group = form.group.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.group.data = current_user.group
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/profile/deed/delete', methods=['GET', 'POST'])
@login_required
def delete_deed():
    id = request.form.get('deedid')
    deed = Deed.query.filter_by(id=id).first_or_404()
    db.session.delete(deed)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))


@app.route("/update", methods=["POST"])
def update():
    id = request.form.get('deedid')
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newcontent = request.form.get("newcontent")
    oldcontent = request.form.get("oldcontent")
    deed = Deed.query.filter_by(id=id).first_or_404()
    deed.title = newtitle
    deed.body = newcontent
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))
