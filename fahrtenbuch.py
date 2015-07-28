from flask import Flask, render_template, url_for, redirect, flash, request, session
import config
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, Fahrt
from database import db_session
from forms import LoginForm, EditPasswordForm, NewFahrtForm, NewUserForm, EditUserForm, EditUserPasswordForm
from hash_passwords import make_hash
from sqlalchemy import asc,func, desc
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
Bootstrap(app)

# Integration von Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.valid_password(form.password.data):
            if login_user(user, remember=form.remember.data):
                session.permanent = not form.remember.data
                flash('Logged in successfully.')
                return redirect(request.args.get('next') or url_for('logged_in'))
            else:
                flash('This account is disabled')
        else:
            flash('Wrong username and / or password')
    return render_template('login.jinja', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('index'))

@app.route("/logged_in")
@login_required
def logged_in():
    return render_template('logged_in.jinja')

@app.route('/password', methods=["GET", "POST"])
@login_required
def password():
    user = User.query.filter_by(id=current_user.id).first()
    form = EditPasswordForm()
    if form.validate_on_submit():
        if user is not None and user.valid_password(form.old_password.data):
            user.password = make_hash(form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Passwort erfolgreich aktualisiert!')
            return redirect(url_for('logged_in'))
        else:
            flash('Passwort nicht aktualisiert! Aktuelles Passwort nicht korrekt!')
    return render_template('password.jinja', form=form)
    
@app.route('/user/add', methods=["GET", "POST"])

def user_add():
    form = NewUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=make_hash(form.password.data), active=form.active.data)
        if new_user:
            db_session.add(new_user)
            db_session.commit()
            flash('Neuer Nutzer erfolgreich angelegt!')
            return redirect(url_for('logged_in'))
        else:
            flash('Neuer Nutzer konnte nicht angelegt werden!')
    return render_template('user_add.jinja', form=form)
    
@app.route('/fahrt/add', methods=["GET", "POST"])
@login_required
def fahrt_add():
    form = NewFahrtForm()
    if form.validate_on_submit():
        new_fahrt = Fahrt(driver=form.driver.data, abfahrtdatum=form.abfahrtdatum.data, abfahrtzeit=form.abfahrtzeit.data, ankunftdatum=form.ankunftdatum.data, ankunftzeit=form.ankunftzeit.data, startort=form.startort.data, zielort=form.zielort.data, reisezweck=form.reisezweck.data, autokennzeichen=form.autokennzeichen.data, kilometerstand=form.kilometerstand.data)
        if new_fahrt:
            db_session.add(new_fahrt)
            db_session.commit()
            flash('Neuer Eintrag erfolgreich angelegt!')
            return redirect(url_for('logged_in'))
        else:
            flash('Neuer Eintrag konnte nicht angelegt werden!')
    return render_template('fahrt_add.jinja', form=form)

@app.route('/user/edit/<user_id>', methods=["GET", "POST"])
@login_required
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db_session.add(user)
        db_session.commit()
        flash('Nutzerdaten erfolgreich aktualisiert!')
        return redirect(url_for('user_list'))
    return render_template('user_edit.jinja', form=form, user=user)

@app.route('/user/password/<user_id>', methods=["GET", "POST"])
@login_required
def user_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditUserPasswordForm()
    if form.validate_on_submit():
        if user is not None:
            user.password = make_hash(form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Passwort erfolgreich aktualisiert!')
            return redirect(url_for('user_list'))
        else:
            flash('Passwort nicht aktualisiert! Aktuelles Passwort nicht korrekt!')
    return render_template('user_password.jinja', form=form, user=user)

@app.route('/fahrt/list')
@login_required
def fahrt_list():
    fahrten = Fahrt.query.all()
    return render_template('fahrt_list.jinja', fahrten=fahrten)

@app.route('/user/list')
@login_required
def user_list():
    users = User.query.order_by(asc('username')).all()
    return render_template('user_list.jinja', users=users)

"""
Auswertungen
"""
#meistbefahrene strecken
def most_driven_tracks(db_session):
    result = db_session.query(Fahrt.startort, Fahrt.zielort, func.count('*')).group_by(Fahrt.startort, Fahrt.zielort).order_by(desc(func.count('*'))).all()
    return result  
#Fahrten und Fahrer mit startort/zielord   
def show_rides_by_user(db_session):
    result = db_session.query(Fahrt.driver,Fahrt.startort, Fahrt.zielort).group_by(Fahrt.driver,Fahrt.startort, Fahrt.zielort).order_by(asc(Fahrt.driver))
    return result
#Fahrten eines Autos
def show_rides_by_car(db_session):
    result = db_session.query(Fahrt.autokennzeichen,Fahrt.startort, Fahrt.zielort).group_by(Fahrt.autokennzeichen,Fahrt.startort, Fahrt.zielort).order_by(asc(Fahrt.autokennzeichen))
    return result  
#Kilometer eines Autos. Wir nehmen immer den letzten Eintrag eines Autos, da dies logischerweise die Gesamtkilometer beinhalten muss    
def kilometers_by_car(db_session):    
    result = db_session.query(Fahrt.autokennzeichen,Fahrt.kilometerstand).group_by(Fahrt.autokennzeichen,Fahrt.kilometerstand, Fahrt.kilometerstand).order_by(asc(Fahrt.autokennzeichen))
    return result  
if __name__ == "__main__":
    #app.run()
    
    print "\n\n------Zum Starten der Webanwendung kommentar bei app.run() loeschen ------\n\n"
    """
    Listen in Listen!
    Zum aktivieren der prints einfach app.run() in der zeile oben auskommentieren,
    damit ihr alles auf der shell sehen koennt
    
    Das mit dem fahrten pro User basiert erstmal auf den testdaten, weil wir bisher den namen des eingeloggten
    User nicht in das Formular automatisch einlesen koennen. Wenn es funktioniert, wird dieser automatisch in
    Fahrt.driver geschrieben 
    """
    show_rides_by_user_result = show_rides_by_user(db_session)
    most_driven_tracks_result = most_driven_tracks(db_session)
    show_rides_by_car_result = show_rides_by_car(db_session)
    kilometers_by_car_result = kilometers_by_car(db_session)
    
    

    print "\nUser mit Fahrt digga"
    for element in show_rides_by_user_result:
        print element

    print "\nStrecken digga"
    for element in most_driven_tracks_result:
        print element
    
    print "\nAutos digga"
    for element in show_rides_by_car_result:
        print element

    #Aus fahrtliste ein kennzeichen waehlen
    dein_kennzeichen = "HS-XY-211"
    print "\nKilometer pro Auto digga"
    for element in kilometers_by_car_result:
        if element[0] == dein_kennzeichen:
            kilometer = element[1]
    print dein_kennzeichen," : ",kilometer
           
            
