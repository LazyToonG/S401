from flask import render_template, request, redirect, url_for, flash
from app import app
from app.controllers.LoginController import reqrole
from app.services.RaspberryService import RaspberryService
import subprocess, ipaddress, time
from app.services.TraductionService import Traductionservice


rs = RaspberryService()

ts = Traductionservice()
#import datetime


@app.route("/admin/add_rasp", methods=["POST"])
@reqrole('admin')
def addRaspberry():
    ip = request.form.get("ipRasp")
    nom = request.form.get("nom")
    

    rasps = rs.montreToutRasp()
    if any(r.ipRasp == ip for r in rasps):
        message=ts.message_langue("Raspberry déjà existant","Raspberry already exists")
        flash(message,"error")
        return redirect(url_for("admin_dashboard"))
    
    try:
        ipaddress.IPv4Address(ip)
        rs.ajoutR(nom, ip)
        subprocess.run(["scp", "-r", "./app/static/rasdata/*", f"{nom}@{ip}:/home/{nom}/musiquali/"])

    except ipaddress.AddressValueError:
        flash("IP invalid", "error")

    
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/action_rasp", methods=["POST"])
@reqrole('admin')
def action_rasp():
    button=request.form.get("action")
    rasp_id = request.form.get("raspberry-select")
    nom = rs.selectRNom(rasp_id)
    ip = rs.selectRIp(rasp_id)

    if rasp_id==None:
        message=ts.message_langue("Pas de Raspberry trouvé","No Raspberry found")
        flash(message, "error")
        return redirect(url_for("admin_dashboard"))
    else : 
        rasp_id = int(rasp_id)
    print("rasp_id :",rasp_id)

    if not rasp_id:
        message=ts.message_langue("Aucun Raspberry sélectionné","No Raspberry selected")
        flash(message, "error")
        return redirect(url_for("admin_dashboard"))
    
    if button=="delete-rasp":
        rs.supprimeR(rasp_id)
        message=ts.message_langue("Raspberry supprimé avec succès","Raspberry successfully deleted")
        flash(message, "success")

    elif button=="envoie-ping":
        print(ip)
        result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        if result.returncode == 0:
            message=ts.message_langue("Ping et initialisation OK","Ping and initialisation OK")
            flash(message, "success")
        else:
            message=ts.message_langue("Erreur lors de l'initialisation","Error during initialisation")
            flash(message, "error")
    #tmp
    elif button=="test":
        if rasp_id==None:
            flash("Pas de Raspberry trouvé", "error")
            return redirect(url_for("admin_dashboard"))
        flash("En cours d'envoi...", "warning") #warning parceque c'est jaune, neutre
        subprocess.run(["rsync", "-avz", "--delete", "-e", "ssh","./app/static/rasdata/",  f"{nom}@{ip}:/home/{nom}/musiquali/"])
        flash("envoyer !", "success")
        time.sleep(5)
        flash("Exécution en cours...", "warning")
        subprocess.run(["ssh", f"{nom}@{ip}", "python3", f"/home/{nom}/musiquali/RAS.py"])
    
    return redirect(url_for("admin_dashboard"))


#-> déplacement dans services/RaspberryService.py

# @app.route("/save_export", methods=["POST"])
# @reqrole('commercial')
# def envoieChaqueChangementPlanning():
#     time.sleep(10)  # Attendre 10 secondes avant d'exécuter la fonction pour s'assurer que le fichier est complètement sauvegardé
#     raspberrys = rs.findAll()
#     for r in raspberrys:
#         if r["ipRasp"] is None or r["nom"] is None:
#             continue  # Ignorer les entrées avec des informations incomplètes
#         subprocess.run(["rsync", "-avz", "--delete", "-e", "ssh","./app/static/rasdata/",  f"{r['nom']}@{r['ipRasp']}:/home/{r['nom']}/musiquali/"])
#         flash("envoyer", "success")
#         time.sleep(5)
#         subprocess.run(["ssh", f"{r['nom']}@{r['ipRasp']}", "python3", f"/home/{r['nom']}/musiquali/RAS.py"])


             


    # today = datetime.datetime.today()

    # if today.weekday() == 0:
    #     subprocess.run(["scp", "-v", "/home/shishkovskiy/Documents/perso_S301_perso/Musiquali.png", identifiant.identifiant_requested+"@"+identifiant.ip_requested+":/home/darragh/Images"])
