from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app import app
from app.controllers.LoginController import reqrole

from app.services.EntrepriseService import EntrepriseService
from app.services.TraductionService import Traductionservice
from app.services.UserService import UserService


es = EntrepriseService()
ts = Traductionservice()
us = UserService()


@app.route("/entreprise", methods=["GET"])
# @reqrole('moderateur')
def entreprise_dashboard():
    traductions = ts.tradEntreprise()
    langue_choisie = ts.getLangue()
    textes = traductions[langue_choisie]

    allEntreprises = es.getAllEntreprises()


    return render_template(
        "entreprise.html",
        entreprises=allEntreprises,
        t=textes
    )

@app.route("/entreprise/delete/<int:idEntreprise>", methods=["POST"])
def delete_entreprise(idEntreprise):
    try:
        us.deleteUserIdentreprise(idEntreprise)
        es.deleteEntreprise(idEntreprise)

        flash("Entreprise supprimée avec succès", "success")

    except Exception as e:
        print("DELETE ERROR:", e)   # 👈 IMPORTANT
        flash(f"Erreur: {e}", "error")

    return redirect(url_for("entreprise_dashboard"))

@app.route("/entreprise/create", methods=["POST"])
def create_entreprise():
    try:
        nomEntreprise = request.form.get("nomEntreprise")

        idEntreprise = es.createEntreprise(nomEntreprise)

        if not idEntreprise:
            raise Exception("Création entreprise échouée")

        flash("Entreprise créée avec succès", "success")

        mail = f"{nomEntreprise}_{idEntreprise}@mail.com"

        us.signin(
            nomEntreprise,
            "admin",
            "admin",
            mail,
            idEntreprise
        )

    except Exception as e:
        print(e)
        flash("Erreur lors de la création de l'entreprise", "error")

    return redirect(url_for("entreprise_dashboard"))