from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, login_manager

import os


app = Flask(__name__)
app.secret_key = 'elsdhfsdlfdsjfkljdslfhjlds'
app.debug = True
login_manager = LoginManager()  # init instance ofhte LoginManager class
login_manager.init_app(app)  # sets up our login for the app
# setting default login view as the login function
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    """ Homepage """
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
