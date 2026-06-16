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



# --- Import et fonction de mot de passe perdu
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def envoyer_email_reset(destinataire, lien_reset):
    # Renseigne ici ton adresse d'envoi (ex: une adresse Gmail de test)
    expediteur = "akihito.mishima2@gmail.com"
    mot_de_passe = "bpnlamgunnehrxxz"

    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = destinataire
    msg['Subject'] = "Réinitialisation de votre mot de passe - Musiquali"

    corps = f"""Bonjour,
    
Vous avez demandé la réinitialisation de votre mot de passe.
Cliquez sur le lien ci-dessous pour le modifier (ce lien est valide 15 minutes) :
{lien_reset}

Si vous n'êtes pas à l'origine de cette demande, veuillez ignorer cet e-mail.

L'équipe Musiquali.
"""
    msg.attach(MIMEText(corps, 'plain', 'utf-8'))

    try:
        # Connexion au serveur de Google
        serveur = smtplib.SMTP('smtp.gmail.com', 587)
        serveur.starttls() # Sécurisation de la connexion
        serveur.login(expediteur, mot_de_passe)
        serveur.send_message(msg)
        serveur.quit()
        print(f"E-mail envoyé avec succès à {destinataire}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False
    
# ---



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
                session["idUtilisateur"] = user.idUtilisateur
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
        return render_template('login.html', msg_error=msg_error, t=textes, current_lang=langue_choisie)

    
    @app.route('/logout')
    @reqlogged
    def logout():
        session.clear()
        message=ts.message_langue("Déconnexion réussie",'Successfully logged out')
        flash(message,'success')
        return redirect(url_for('login'))


    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        traductions = ts.tradPassword()
        langue_choisie = ts.getLangue()
        textes = traductions[langue_choisie]

        if request.method == 'POST':
            email = request.form.get('email')
            
            # 1. On cherche si l'utilisateur existe avec cet e-mail
            user = us.getUserByEmail(email)
            
            if user:
                # 2. On crée le sérialiseur avec la clé secrète de l'application
                s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
                
                # 3. On génère un jeton crypté contenant l'e-mail de l'utilisateur
                token = s.dumps(email, salt='password-reset-salt')
                
                # 4. On génère l'URL absolue que l'utilisateur devra visiter
                # (Cette route /reset_password/<token> sera créée juste après)
                link = url_for('reset_password', token=token, _external=True)
                
                envoyer_email_reset(email, link)
                
            # 5. Sécurité : Qu'un e-mail existe ou pas, on affiche TOUJOURS le même message.
            # Cela empêche les personnes malveillantes de deviner quels e-mails ont un compte.
            message = ts.message_langue(
                "Si cette adresse existe, un e-mail de réinitialisation a été envoyé.",
                "If this address exists, a reset email has been sent."
            )
            flash(message, "success")
            return redirect(url_for('login'))
            
        return render_template('forgot_password.html', t=textes)
    

    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        traductions = ts.tradPassword()
        langue_choisie = ts.getLangue()
        textes = traductions[langue_choisie]

        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        
        try:
            # On tente de lire le jeton. S'il a plus de 15 minutes (900s), ça lève une exception.
            email = s.loads(token, salt='password-reset-salt', max_age=900)
        except SignatureExpired:
            flash("Le lien de réinitialisation a expiré (valide 15 min). Veuillez recommencer.", "error")
            return redirect(url_for('forgot_password'))
        except BadTimeSignature:
            flash("Lien de réinitialisation invalide ou corrompu.", "error")
            return redirect(url_for('forgot_password'))
            
        # Si le jeton est valide, on s'assure que l'utilisateur est toujours là
        user = us.getUserByEmail(email)
        if not user:
            flash("Utilisateur introuvable.", "error")
            return redirect(url_for('forgot_password'))

        if request.method == 'POST':
            nouveau_mdp = request.form.get('password')
            conf_mdp = request.form.get('confirm_password')
            
            if nouveau_mdp != conf_mdp:
                flash("Les mots de passe ne correspondent pas.", "error")
                return render_template('reset_password_form.html', token=token, t=textes)
                
            us.setPassword(user.username, nouveau_mdp)
        
            flash("Votre mot de passe a été modifié avec succès ! Vous pouvez vous connecter.", "success")
            return redirect(url_for('login'))
            
        # Si c'est un GET, on affiche un petit formulaire pour taper le nouveau mot de passe
        # (On va créer ce fichier HTML juste en dessous)
        return render_template('reset_password_form.html', token=token, t=textes)