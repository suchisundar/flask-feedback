from flask import Flask, request, redirect, render_template, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import FeedbackForm, RegisterForm, LoginForm, DeleteForm
from werkzeug.exceptions import Unauthorized

from models import connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = 'SECRETSECRETSECRET'
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    '''Homepage of site, redirect to register'''

    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register_user():
    '''Show user form and process form by adding a new user'''

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password,first_name,last_name,email)

        
        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('users/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    '''Show login form and process the login form'''

    form = LoginForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username,password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout_user():
    '''Logout user'''

    session.pop("username")
    return redirect('/login')


@app.route('/users/<username>')
def show_user(username):
    '''Example page for logged-in-users'''

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form=DeleteForm()

    return render_template('users/show.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=["POST"])
def remove_user_feedback(username):
    '''Remove user and redirect to login'''
    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    user = User.query.delete()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')


@app.route('/users/<username>/feedback/new', methods=["GET", "POST"])
def add_feedback(username):
    '''Display feedback form and process'''

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content=form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username)

        db.session.add(feedback)
        db.session.commit()

        # return redirect(f'/users/{feedback.username}')
        return redirect(url_for('show_user', username=feedback.username))
    else:
        return render_template('feedback/new.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    '''Display form to edit feedback'''

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

       
        return redirect(url_for('show_user', username=feedback.username))
   
    return render_template('feedback/edit.html', form=form, feedback=feedback)


