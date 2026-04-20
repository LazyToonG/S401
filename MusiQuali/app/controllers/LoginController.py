from flask import render_template, redirect, url_for, request
from flask import session, flash, abort
from app import app
from functools import wraps
from app.services.UserService import UserService
from app.services.TraductionService import Traductionservice

ts = Traductionservice()

us = UserService()

def reqlogged(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            flash('Denied. You need to login.')
            return redirect(url_for('login'))
    return wrap


def reqrole(*role):
    """
    Décorateur vérifiant si l'utilisateur est connecté et s'il a le rôle requis.
    """
    def wrap(f):
        @wraps(f)
        def verifyRole(*args, **kwargs):
            if not session.get('logged'):
                return redirect(url_for('login'))

            current_role = session.get('role')
            if current_role not in role:
                abort(403)
            return f(*args, **kwargs)
        return verifyRole
    return wrap


class LoginController:

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        traductions=ts.tradLogin()

        langue_choisie=ts.getLangue()
        textes = traductions[langue_choisie]
        
        msg_error = None
        if request.method == 'POST':
            user = us.login(request.form["username"], request.form["password"])
            if user:
                session["logged"] = True
                session["username"] = user.username
                session["role"] = user.role
                if user.role == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif user.role == "marketing":
                    return redirect(url_for("marketing"))
                elif user.role == "commercial":
                    return redirect(url_for("voir_planning"))
                else:
                    return redirect(url_for("index"))
            else:
                msg_error = ts.message_langue('Identifiants non valides','Invalid Credentials')
        return render_template('login_v2.html', msg_error=msg_error, t=textes, current_lang=langue_choisie)

    @app.route("/admin/create_user", methods=['GET', 'POST'])
    def signin():

        traductions=ts.tradAdmin()

        langue_choisie=ts.getLangue()
        textes = traductions[langue_choisie]

        user=session['username']
        role=session['role']

        if request.method == "POST":
            user_1 = request.form["username"]
            password_1 = request.form["password"]
            role_1 = request.form.get("role", "commercial")

            result = us.signin(user_1, password_1, role_1)
            if not result:
                return render_template("admin.html", msg_error="creation error", t=textes, current_lang=langue_choisie, user=user, role=role)
            else:
                return render_template("admin.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
        else:
            return render_template('admin.html', msg_error=None, t=textes, current_lang=langue_choisie, user=user, role=role)

    @app.route('/logout')
    @reqlogged
    def logout():
        session.clear()
        message=ts.message_langue("Déconnexion réussie",'Successfully logged out')
        flash(message,'success')
        return redirect(url_for('login'))
