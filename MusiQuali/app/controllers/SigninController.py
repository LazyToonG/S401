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
        traductions = ts.tradSignin()
        langue_choisie = ts.getLangue()
        textes = traductions[langue_choisie]

        # Initialisation par défaut pour éviter l'erreur "variable referenced before assignment"
        user = None
        role = None

        if session.get('logged'):
            user = session.get('username')
            role = session.get('role')

        if request.method == "POST":
            user_1 = request.form.get("username")
            password_1 = request.form.get("password")
            confirm_password = request.form.get("confirm_password") # On récupère la confirmation
            role_1 = request.form.get("role", "commercial")
            mail_1 = request.form.get("email")

            # 1. Vérification des mots de passe
            if password_1 != confirm_password:
                message = ts.message_langue("Les mots de passe ne correspondent pas", "Passwords do not match")
                flash(message, "error")
                return render_template("signin.html", msg_error="password mismatch", t=textes, current_lang=langue_choisie)

            # 2. Tentative de création dans la base de données
            result = us.signin(user_1, password_1, role_1, mail_1)
            
            if not result and session.get('logged'):
                # Un admin tente de créer mais échoue
                flash("Erreur : Impossible de créer l'utilisateur.", "error")
                return render_template("admin.html", msg_error="creation error", t=textes, current_lang=langue_choisie, user=user, role=role)
            
            elif result and session.get('logged'):
                # Un admin réussit à créer
                flash("Utilisateur créé avec succès !", "success")
                if role_1 == "admin":
                    return render_template("admin.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
                if role_1 == "marketing":
                    return render_template("marketing.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
                if role_1 == "commercial":
                    return render_template("commercial.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
            
            elif not result:
                # Un visiteur tente de s'inscrire mais échoue (pseudo/mail déjà pris)
                message = ts.message_langue("Erreur : Nom d'utilisateur ou email déjà existant.", "Error: Username or email already exists.")
                flash(message, "error")
                return render_template("signin.html", msg_error="creation error", t=textes, current_lang=langue_choisie)
            
            else:
                # Un visiteur s'inscrit avec succès !
                session["logged"] = True
                session["username"] = user_1
                session["role"] = role_1
                
                # On utilise role_1 ici (et non user.role)
                if role_1 == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif role_1 == "marketing":
                    return redirect(url_for("marketing"))
                elif role_1 == "commercial":
                    return redirect(url_for("voir_planning"))
                    
        else:
            if session.get('logged'):
                return render_template('admin.html', msg_error=None, t=textes, current_lang=langue_choisie, user=user, role=role)
            else:
                return render_template('signin.html', msg_error=None, t=textes, current_lang=langue_choisie)