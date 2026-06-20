from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app import app
from app.controllers.LoginController import reqrole
from app.controllers.RaspberryController import etatPing, dernierOk
from app.services.LogsService import LogsService

from app.services.UserService import UserService
from app.services.RaspberryService import RaspberryService
from app.services.TraductionService import Traductionservice
from app.DAO.RequeteDAO import RequeteDAO

rs = RaspberryService()
ls = LogsService()
ts = Traductionservice()
user_service = UserService()
req_dao = RequeteDAO()


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def envoyer_email_decision(destinataire, pseudo, type_requete, accepte=True):
    expediteur = "akihito.mishima2@gmail.com"
    mot_de_passe = "bpnlamgunnehrxxz"

    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = destinataire

    # Personnalisation du sujet et du corps selon la décision
    if accepte:
        msg['Subject'] = "Votre demande a été acceptée ! - Musiquali"
        if type_requete == "inscription":
            corps = f"""Bonjour {pseudo},

Bonne nouvelle ! Votre demande d'inscription sur Musiquali a été acceptée par l'administrateur.
Vous pouvez dès à présent vous connecter à votre compte en utilisant vos identifiants.

L'équipe Musiquali.
"""
        else:
            corps = f"""Bonjour {pseudo},

Votre demande concernant l'action : "{type_requete}" a bien été acceptée et traitée par l'administrateur.

L'équipe Musiquali.
"""
    else:
        msg['Subject'] = "Mise à jour concernant votre demande - Musiquali"
        corps = f"""Bonjour {pseudo},

Nous vous informons que votre demande concernant l'action : "{type_requete}" n'a pas pu être acceptée par l'administrateur.

Pour toute question ou réclamation, veuillez contacter directement votre responsable d'équipe.

L'équipe Musiquali.
"""

    msg.attach(MIMEText(corps, 'plain', 'utf-8'))

    try:
        serveur = smtplib.SMTP('smtp.gmail.com', 587)
        serveur.starttls()
        serveur.login(expediteur, mot_de_passe)
        serveur.send_message(msg)
        serveur.quit()
        print(f"E-mail de notification envoyé avec succès à {destinataire}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail de décision : {e}")
        return False


@app.route("/admin", methods=["GET"])
@reqrole('admin')
def admin_dashboard():
    traductions = ts.tradAdmin()
    langue_choisie = ts.getLangue()
    textes = traductions[langue_choisie]

    user = session['username']
    role = session['role']
    id_entreprise = session.get('idEntreprise', 1)

    # --- TRI DES RASPBERRY ---
    current_sort_rasp = request.args.get('sort_rasp')

    if current_sort_rasp == 'asc':
        rasp = rs.triASC()
    elif current_sort_rasp == 'desc':
        rasp = rs.triDESC()
    elif current_sort_rasp == 'ip':
        rasp = rs.triIP()
    else:
        rasp = rs.montreToutRasp()

    # --- TRI DES UTILISATEURS ---
    logs_by_rasp = {}

    for r in rasp:
        logs_by_rasp[r.nomLecteur] = ls.list_log_files(r.nomLecteur)

    current_sort = request.args.get('sort')
    if current_sort == 'asc':
        users = user_service.triASC(id_entreprise)
    elif current_sort == 'desc':
        users = user_service.triDESC(id_entreprise)
    elif current_sort == 'role':
        users = user_service.triRole(id_entreprise)
    else:
        users = user_service.getUsers(id_entreprise)

    requetes = req_dao.lire_json()

    return render_template(
        "admin.html",
        raspberry=rasp,
        users=users,
        logs_by_rasp=logs_by_rasp,
        requetes=requetes,
        t=textes,
        current_lang=langue_choisie,
        user=user,
        role=role,
        current_sort=current_sort,
        current_sort_rasp=current_sort_rasp,
        etatPing=etatPing,
        dernierOk=dernierOk
    )

#LOGS

@app.route("/admin/api/logs/<nom>")
@reqrole('admin')
def api_list_logs(nom):
    """Retourne en JSON la liste des fichiers logs d'un lecteur."""
    files = ls.list_log_files(nom)
    return jsonify({"nom": nom, "files": files})


@app.route("/admin/api/log/<nom>/<filename>")
@reqrole('admin')
def api_read_log(nom, filename):
    """Retourne en JSON le contenu d'un fichier log précis."""
    content = ls.read_log_file(nom, filename)
    if content is None:
        return jsonify({"error": "Fichier introuvable"}), 404
    return jsonify({"nom": nom, "filename": filename, "content": content})

# Création utilisateur

@app.route("/admin/create", methods=["POST", "GET"])
@reqrole('admin')
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")
    mail = request.form.get("email")
    entreprise = session["idEntreprise"]

    if not username or not password or not role:
        flash("Tous les champs sont obligatoires", "error")
        return redirect(url_for("admin_dashboard"))
    searched_users = user_service.getUserByUsername(username, entreprise)

    for users in searched_users:
        if users!=None:
            if users.username==username:
                message=ts.message_langue("Nom d'utilisateur déjà existant","Username already exists")
                flash(message, "error")
                return redirect(url_for("admin_dashboard"))
                
    user_service.signin(username, password, role, mail, entreprise)

    message=ts.message_langue("Utilisateur créé avec succès","User successfully created")
    flash(message, "success")
    return redirect(url_for("admin_dashboard", _anchor="users"))

#suppression utilisateur
@app.route("/admin/delete", methods=["POST"])
@reqrole('admin')
def delete_user():
    user=session['username']
    id_entreprise = session.get('idEntreprise', 1)

    decision=request.form.get("decision")
    if decision=="cancel" :
        return redirect(url_for("admin_dashboard", _anchor="users"))
    
    username = request.form.get("username")

    if username==user:
        return redirect(url_for("admin_dashboard", _anchor="users"))
    
    user_service.deleteUser(username, id_entreprise)

    return redirect(url_for("admin_dashboard", _anchor="users"))

@app.route("/admin/search", methods=["POST", "GET"])
@reqrole('admin')
def admin_search_user():
    traductions=ts.tradAdmin()

    langue_choisie=ts.getLangue()
    textes = traductions[langue_choisie]

    requetes = req_dao.lire_json()

    user=session['username']
    role=session['role']
    username = request.form.get("username")
    id_entreprise = session.get('idEntreprise', 1)

    if not username:
        return redirect(url_for("admin_dashboard", _anchor="users"))

    searched_users = user_service.getUserByUsername(username, id_entreprise)
    for users in searched_users:
        if users==None:
            message=ts.message_langue("Utilisateur non trouvé","User not found")
            flash(message, "error")
            return redirect(url_for("admin_dashboard"))
    message=ts.message_langue("Utilisateur trouvé avec succès","User successfully found")
    flash(message, "success")
    return render_template("admin.html",searched_users=searched_users, t=textes, current_lang=langue_choisie, user=user, role=role, requetes=requetes)

@app.route("/admin/edit_user", methods=["POST"])
@reqrole('admin')
def edit_user():
    id_entreprise = session.get('idEntreprise', 1)
    ancien_username = request.form.get("original_username")
    ancien_email = request.form.get("original_email")
    nouveau_username = request.form.get("edit_username")
    nouvel_email = request.form.get("edit_email")

    if nouvel_email != ancien_email:
        user_service.setEmail(ancien_username, nouvel_email, id_entreprise)
        ancien_email = nouvel_email 

    if nouveau_username != ancien_username:
        user_service.setUsername(ancien_username, nouveau_username, id_entreprise)

    message = ts.message_langue("Utilisateur mis à jour !", "User updated!")
    flash(message, "success")
    return redirect(url_for("admin_dashboard", _anchor="users"))


@app.route("/admin/api/search_users", methods=["GET"])
@reqrole('admin')
def api_search_users():
    traductions = ts.tradAdmin()
    langue_choisie = ts.getLangue()
    textes = traductions[langue_choisie]

    id_entreprise = session.get('idEntreprise', 1)

    requetes = req_dao.lire_json()

    query = request.args.get('q', '')
    
    if query == '':
        users = user_service.getUsers(id_entreprise)
    else:
        users = user_service.recherche(query, id_entreprise)
        
    # On renvoie UNIQUEMENT le morceau de HTML (le partial)
    return render_template("partials/admin_users_list.html", users=users, t=textes, requetes=requetes)

@app.route("/admin/api/search_rasp", methods=["GET"])
@reqrole('admin')
def api_search_rasp():
    traductions = ts.tradAdmin()
    langue_choisie = session.get('lang', ts.getLangue()) 
    textes = traductions[langue_choisie]

    requetes = req_dao.lire_json()
    
    query = request.args.get('q', '')
    
    if query == '':
        raspberry = rs.montreToutRasp()
    else:
        raspberry = rs.recherche(query)
        
    return render_template("partials/admin_rasp_list.html", 
                           raspberry=raspberry, 
                           t=textes,
                           requetes=requetes,
                           etatPing=etatPing,
                           dernierOk=dernierOk)


# --- GESTION DES REQUETES (Accepter / Refuser) ---
@app.route("/admin/action_requete", methods=["POST"])
@reqrole('admin')
def action_requete():
    req_id = request.form.get("req_id")
    action = request.form.get("action")
    
    requetes = req_dao.lire_json()
    
    if req_id not in requetes:
        flash("Cette requête n'existe plus.", "error")
        return redirect(url_for("admin_dashboard", _anchor="requests"))
        
    req = requetes[req_id]
    type_req = req.get('type')
    mail_dest = req.get('mail')
    pseudo_dest = req.get('demandeur')
    
    if action == "accept" :
        if type_req == "inscription":
            user_service.signin(req.get('demandeur'), req.get('mdp'), req.get('role'), req.get('mail'), req.get('entreprise'))
            flash(f"La requête a été acceptée et le compte de {req.get('demandeur')} a été créé !", "success")
        else:
            flash(f"La requête a été marquée comme traitée. Pensez à appliquer les changements pour {req.get('demandeur')} dans 'Gestion des utilisateurs'.", "success")

        envoyer_email_decision(mail_dest, pseudo_dest, type_req, accepte=True)
        
    elif action == "refuse":
        flash(f"La requête de {req.get('demandeur')} a été refusée.", "success")

        envoyer_email_decision(mail_dest, pseudo_dest, type_req, accepte=False)
    
    del requetes[req_id]
    req_dao.ecrire_json(requetes)
    
    return redirect(url_for("admin_dashboard", _anchor="requests"))