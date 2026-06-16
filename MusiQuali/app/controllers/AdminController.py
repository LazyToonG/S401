from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app import app
from app.controllers.LoginController import reqrole
from app.controllers.RaspberryController import etatPing, dernierOk
from app.services.LogsService import LogsService

from app.services.UserService import UserService
from app.services.RaspberryService import RaspberryService
from app.services.TraductionService import Traductionservice

rs = RaspberryService()
ls = LogsService()
ts = Traductionservice()
user_service = UserService()


@app.route("/admin", methods=["GET"])
@reqrole('admin')
def admin_dashboard():

    traductions=ts.tradAdmin()
    langue_choisie=ts.getLangue()
    textes = traductions[langue_choisie]

    user=session['username']
    role=session['role']

    rasp = rs.montreToutRasp()

    logs_by_rasp = {}

    for r in rasp:
        logs_by_rasp[r.nom] = ls.list_log_files(r.nom)

    current_sort = request.args.get('sort')

    if current_sort == 'asc':
        users = user_service.triASC()
    elif current_sort == 'desc':
        users = user_service.triDESC()
    elif current_sort == 'role':
        users = user_service.triRole()
    else:
        users = user_service.getUsers()

    return render_template(
        "admin.html",
        raspberry=rasp,
        users=users,
        logs_by_rasp=logs_by_rasp,
        t=textes,
        current_lang=langue_choisie,
        user=user,
        role=role,
        current_sort=current_sort,
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

    if not username or not password or not role:
        flash("Tous les champs sont obligatoires", "error")
        return redirect(url_for("admin_dashboard"))
    searched_users = user_service.getUserByUsername(username)

    for users in searched_users:
        if users!=None:
            if users.username==username:
                message=ts.message_langue("Nom d'utilisateur déjà existant","Username already exists")
                flash(message, "error")
                return redirect(url_for("admin_dashboard"))
                
    user_service.signin(username, password, role)

    message=ts.message_langue("Utilisateur créé avec succès","User successfully created")
    flash(message, "success")
    return redirect(url_for("admin_dashboard", _anchor="users"))

#suppression utilisateur
@app.route("/admin/delete", methods=["POST"])
@reqrole('admin')
def delete_user():
    user=session['username']

    decision=request.form.get("decision")
    if decision=="cancel" :
        return redirect(url_for("admin_dashboard", _anchor="users"))
    
    username = request.form.get("username")

    if username==user:
        return redirect(url_for("admin_dashboard", _anchor="users"))
    
    user_service.deleteUser(username)

    return redirect(url_for("admin_dashboard", _anchor="users"))

@app.route("/admin/search", methods=["POST", "GET"])
@reqrole('admin')
def admin_search_user():
    traductions=ts.tradAdmin()

    langue_choisie=ts.getLangue()
    textes = traductions[langue_choisie]

    user=session['username']
    role=session['role']
    username = request.form.get("username")

    if not username:
        return redirect(url_for("admin_dashboard", _anchor="users"))

    searched_users = user_service.getUserByUsername(username)
    for users in searched_users:
        if users==None:
            message=ts.message_langue("Utilisateur non trouvé","User not found")
            flash(message, "error")
            return redirect(url_for("admin_dashboard"))
    message=ts.message_langue("Utilisateur trouvé avec succès","User successfully found")
    flash(message, "success")
    return render_template("admin.html",searched_users=searched_users, t=textes, current_lang=langue_choisie, user=user, role=role)

@app.route("/admin/edit_user", methods=["POST"])
@reqrole('admin')
def edit_user():
    ancien_username = request.form.get("original_username")
    ancien_email = request.form.get("original_email")
    nouveau_username = request.form.get("edit_username")
    nouvel_email = request.form.get("edit_email")

    if nouvel_email != ancien_email:
        user_service.setEmail(ancien_username, nouvel_email)
        ancien_email = nouvel_email 

    if nouveau_username != ancien_username:
        user_service.setUsername(ancien_username, nouveau_username)

    message = ts.message_langue("Utilisateur mis à jour !", "User updated!")
    flash(message, "success")
    return redirect(url_for("admin_dashboard", _anchor="users"))