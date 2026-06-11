from flask import render_template, redirect, url_for, request
from flask import session, flash, abort
from app import app
from app.services.UserService import UserService
from app.services.TraductionService import Traductionservice

ts = Traductionservice()

us = UserService()

class SigninController:

    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        traductions=ts.tradSignin()

        langue_choisie=ts.getLangue()
        textes = traductions[langue_choisie]

        if session.get('logged'):
            user=session['username']
            role=session['role']

        if request.method == "POST":
            user_1 = request.form["username"]
            password_1 = request.form["password"]
            role_1 = request.form.get("role", "commercial")

            result = us.signin(user_1, password_1, role_1)
            if not result and session.get('logged'):
                return render_template("admin.html", msg_error="creation error", t=textes, current_lang=langue_choisie, user=user, role=role)
            elif result and session.get('logged'):
                if role_1=="admin":
                    return render_template("admin.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
                if role_1=="marketing":
                    return render_template("marketing.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
                if role_1=="commercial":
                    return render_template("commercial.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
            elif not result:
                return render_template("signin.html", msg_error="creation error", t=textes, current_lang=langue_choisie)
            else:
                session["logged"] = True
                session["username"] = user_1
                session["role"] = role_1
                if user.role == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif user.role == "marketing":
                    return redirect(url_for("marketing"))
                elif user.role == "commercial":
                    return redirect(url_for("voir_planning"))
        else:
            if session.get('logged'):
                return render_template('admin.html', msg_error=None, t=textes, current_lang=langue_choisie, user=user, role=role)
            else:
                return render_template('signin.html', msg_error=None, t=textes, current_lang=langue_choisie)
