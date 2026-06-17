from flask import render_template, request, session, redirect, url_for, flash
from app import app
from app.controllers.LoginController import reqrole

from app.services.UserService import UserService
from app.services.TraductionService import Traductionservice

ts = Traductionservice()
us = UserService()

class SettingsController:

    @app.route('/profile', methods=['GET'])
    def profile():
        # Sécurité : vérifier que l'utilisateur est bien connecté
        if not session.get('logged'):
            return redirect(url_for('login'))

        traductions = ts.tradProfil()
        langue_choisie = session.get('lang', 'fr')
        textes = traductions[langue_choisie]
        
        user = session['username']
        role = session['role']

        # On récupère toutes les infos de l'utilisateur (dont l'email)
        user_info_list = us.getUserByUsername(user)
        user_info = user_info_list[0] if user_info_list else None

        # On passe 'user_info' à notre template HTML
        return render_template('profile.html', user=user, role=role, user_info=user_info, t=textes, current_lang=langue_choisie)
    
    
    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        if not session.get('logged'):
            return redirect(url_for('login'))

        # On utilise la session pour savoir QUI on modifie (très sécurisé !)
        ancien_username = session['username']
        
        nouveau_username = request.form.get('username')
        nouvel_email = request.form.get('email')

        user_info_list = us.getUserByUsername(ancien_username)
        user_info = user_info_list[0] if user_info_list else None

        if user_info:
            # 1. Mise à jour de l'email si modifié
            if nouvel_email and nouvel_email != user_info.mail:
                us.setEmail(ancien_username, nouvel_email)
            
            # 2. Mise à jour du nom d'utilisateur si modifié
            if nouveau_username and nouveau_username != ancien_username:
                us.setUsername(ancien_username, nouveau_username)
                # CRUCIAL : On met à jour la session avec le nouveau nom !
                session['username'] = nouveau_username
        
        flash("Votre profil a été mis à jour avec succès !", "success")
        return redirect(url_for('profile'))
    
    
    @app.route('/update_password', methods=['POST'])
    def update_password():
        if not session.get('logged'):
            return redirect(url_for('login'))

        username = session['username']
        ancien_mdp = request.form.get('old_password')
        nouveau_mdp = request.form.get('new_password')
        conf_mdp = request.form.get('confirm_password')

        # 1. On utilise ta fonction login existante pour vérifier si l'ancien mot de passe tapé est le bon !
        user_valid = us.login(username, ancien_mdp)
        
        if not user_valid:
            flash("L'ancien mot de passe est incorrect.", "error")
            return redirect(url_for('profile'))

        # 2. On vérifie que le nouveau mot de passe a bien été confirmé sans faute de frappe
        if nouveau_mdp != conf_mdp:
            flash("Les nouveaux mots de passe ne correspondent pas.", "error")
            return redirect(url_for('profile'))

        # 3. Si tout est bon, on utilise la méthode setPassword (qui hache déjà le MDP grâce à notre précédente correction !)
        us.setPassword(username, nouveau_mdp)
        
        flash("Votre mot de passe a été modifié avec succès !", "success")
        return redirect(url_for('profile'))


    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        if not session.get('logged'):
            return redirect(url_for('login'))

        traductions = ts.tradSettings() 
        
        langue_choisie = session.get('lang', 'fr')
        textes = traductions[langue_choisie]
        
        user = session['username']
        role = session['role']

        if request.method == 'POST':
            langue = request.form.get('language')
            dark_mode = request.form.get('dark_mode')
            
            # --- SAUVEGARDE DE LA LANGUE ---
            if langue in ['fr', 'en']:
                session['lang'] = langue  # On l'enregistre directement ici !
            
            flash("Vos préférences ont été enregistrées.", "success")
            return redirect(url_for('settings'))

        return render_template('settings.html', user=user, role=role, t=textes, current_lang=langue_choisie)