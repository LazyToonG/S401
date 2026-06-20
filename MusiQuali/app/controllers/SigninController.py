from flask import render_template, redirect, url_for, request
from flask import session, flash, abort
from app import app
from app.services.UserService import UserService
from app.services.EntrepriseService import EntrepriseService
from app.services.TraductionService import Traductionservice

from app.DAO.RequeteDAO import RequeteDAO
req_dao = RequeteDAO()

ts = Traductionservice()

es = EntrepriseService()
us = UserService()

class SigninController:

    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        traductions = ts.tradSignin()
        langue_choisie = ts.getLangue()
        textes = traductions[langue_choisie]

        entreprises = es.getAllEntreprises()

        user = None
        role = None

        if session.get('logged'):
            user = session.get('username')
            role = session.get('role')

        if request.method == "POST":
            user_1 = request.form.get("username")
            password_1 = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            role_1 = request.form.get("role", "commercial")
            mail_1 = request.form.get("email")
            entreprise_1 = request.form.get("entreprise") # <-- 1. On récupère l'entreprise

            # Vérification des mots de passe
            if password_1 != confirm_password:
                message = ts.message_langue("Les mots de passe ne correspondent pas", "Passwords do not match")
                flash(message, "error")
                return render_template("signin.html", msg_error="password mismatch", t=textes, current_lang=langue_choisie, entreprises=entreprises)

            # --- CAS 1 : UN ADMINISTRATEUR CRÉE LE COMPTE DIRECTEMENT ---
            if session.get('logged') and role == "admin":
                # On crée l'utilisateur de suite (avec entreprise_1)
                result = us.signin(user_1, password_1, role_1, mail_1, entreprise_1)
                
                if result:
                    flash("Utilisateur créé avec succès !", "success")
                    return render_template("admin.html", msg_error="user created", t=textes, current_lang=langue_choisie, user=user, role=role)
                else:
                    flash("Erreur : Impossible de créer l'utilisateur.", "error")
                    return render_template("admin.html", msg_error="creation error", t=textes, current_lang=langue_choisie, user=user, role=role)

            # --- CAS 2 : UN VISITEUR DEMANDE À S'INSCRIRE ---
            else:
                # 1. On prépare le message
                sujet_req = "inscription"
                contenu_req = f"L'utilisateur {user_1} souhaite rejoindre l'entreprise {entreprise_1} avec le rôle {role_1}."
                
                # 2. On sauvegarde dans le JSON !
                req_dao.ajouter_requete(
                    demandeur=user_1, 
                    mail=mail_1, 
                    type_req=sujet_req, 
                    message=contenu_req, 
                    role=role_1, 
                    entreprise=entreprise_1, 
                    mdp=password_1 # Idéalement, crypte-le avant de le stocker ici !
                )

                # 3. Message de succès pour le visiteur
                message = ts.message_langue(
                    "Votre demande d'inscription a bien été envoyée à l'administrateur.", 
                    "Your registration request has been sent."
                )
                flash(message, "success")
                
                return redirect(url_for("signin"))
                    
        else:
            if session.get('logged'):
                return render_template('admin.html', msg_error=None, t=textes, current_lang=langue_choisie, user=user, role=role)
            else:
                return render_template('signin.html', msg_error=None, t=textes, current_lang=langue_choisie, entreprises=entreprises)