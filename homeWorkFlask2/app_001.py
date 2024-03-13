from flask import Flask, session, make_response, render_template, redirect, url_for, request

app = Flask(__name__)


app.secret_key = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route("/")
@app.route('/page_main/')
def page_main():
    context = {'title': 'Главная страница'}
    return render_template('page_main.html', **context)


@app.route('/name_email/', methods=["POST", "GET"])
def name_email():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        session['name'] = name
        session['email'] = email
        context = {'title': 'Доступ...', 'name': name, 'email': email}
        response = make_response(render_template('greetings.html', **context))
        print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
        return response
    context = {'title': 'Знакомство с пользователем'}
    return render_template('name_email.html', **context)


@app.route('/logout/')
def logout():
    print(" --- Сессия ---")
    print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
    session.pop('name', None)
    session.pop('email', None)
    print(" --- Сессия завершена ! ---")
    print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
    return redirect(url_for('name_email'))


if __name__ == "__main__":
    app.run(debug=True)