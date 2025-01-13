from flask import Flask, request, make_response, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash  # Afegim la funció per comprovar la contrasenya
from app import create_app
from app.forms import LoginForm

app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/index', methods=['GET', 'POST'])
def index():
    # Verificar si la cookie de sessió existeix
    if 'user_ip' not in session:
        # Si no existeix, crear una nova cookie, reiniciar la sessió i mostrar un missatge d’avís
        user_ip_information = request.remote_addr
        session["user_ip"] = user_ip_information
        flash("Sessió iniciada. El teu IP s'ha registrat.")
        return redirect('/index')  # Redirigir a la mateixa ruta
    
    # Si ja existeix la cookie, recuperar la IP emmagatzemada
    user_ip = session.get("user_ip")
    username = session.get("username")

    # Crear una instància de LoginForm
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        # Si l'usuari envia el formulari de login, obtenir el nom d'usuari i contrasenya
        username_input = login_form.username.data
        password_input = login_form.password.data
        
        # Comprovar si l'usuari existeix a la base de dades
        user = User.query.filter_by(username=username_input).first()
        
        if user:
            # Si l'usuari existeix, comprovar si la contrasenya és correcta
            if check_password_hash(user.password, password_input):
                session["username"] = username_input
                flash("Has iniciat sessió correctament.")
                return redirect('/index')
            else:
                flash("Contrasenya incorrecta.")
        else:
            flash("No s'ha trobat cap usuari amb aquest nom.")
    
    # Passar la informació al context per mostrar-la a la plantilla
    context = {
        'ip': user_ip,
        'login_form': login_form,
        'username': username
    }

    return render_template("information.html", **context)


# Ruta per la pàgina de Parkings
@app.route('/parkings')
def parkings():
    return render_template('parkings.html')


# Ruta per la pàgina de Perfil d'usuari
@app.route('/perfil')
def perfil_usuario():
    return render_template('perfil.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=81, debug=True)