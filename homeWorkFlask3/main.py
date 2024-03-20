from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash

from forms import RegisterForm
from flask import Flask, render_template, request
from models import db, Users


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase_users.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('All done')


@app.route("/")
@app.route('/page_main/')
def page_main():
    context = {'title': 'Главная страница'}
    return render_template('page_main.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = generate_password_hash(request.form['password'])
        user = Users(name=name, surname=surname, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return f'All done'

    return render_template('register.html', form=form)

