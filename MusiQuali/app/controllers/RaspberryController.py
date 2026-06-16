from pathlib import Path

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.controllers.LoginController import reqrole
from app.services.RaspberryService import RaspberryService
import subprocess, ipaddress, time
from app.services.TraductionService import Traductionservice
import time
from app.services.LogsService import LogsService



rs = RaspberryService()
ls = LogsService()

ts = Traductionservice()
#import datetime


@app.route("/admin/add_rasp", methods=["POST"])
@reqrole('admin')
def addRaspberry():#manque trad pour les flash
    ip = request.form.get("ip")
    nom = request.form.get("nomLecteur")
    mdp = request.form.get("mdpRasp")
    

    rasps = rs.montreToutRasp()
    if any(r.ip == ip for r in rasps):
        message=ts.message_langue("Raspberry déjà existant","Raspberry already exists")
        flash(message,"error")
        return redirect(url_for("admin_dashboard"))
    
    try:
        try:
            print(f"Vérification de l'IP : {ip}")
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            flash("IP invalide", "error")
            return redirect(url_for("admin_dashboard"))
        # subprocess.run(["scp", "-r", "./app/static/rasdata/*", f"{nom}@{ip}:/home/{nom}/musiquali/"])
        # print(f"sshpass -p {mdp} ssh-copy-id -o StrictHostKeyChecking=no {nom}@{ip}")
        subprocess.run(["sshpass", "-p", mdp, "ssh-copy-id", "-o", "StrictHostKeyChecking=no", f"{nom}@{ip}"], check=True, timeout=8, capture_output=True, text=True)

    except subprocess.TimeoutExpired:
        flash("Délai dépassé : le Raspberry ne répond pas", "error")
        return redirect(url_for("admin_dashboard"))
    
    except subprocess.CalledProcessError as e:
        error = (e.stderr or "").lower()

        if "permission denied" in error:
            flash("Mot de passe SSH incorrect", "error")
        elif "connection refused" in error:
            flash("Connexion refusée (SSH off ?)", "error")
        elif "no route to host" in error:
            flash("Raspberry inaccessible", "error")
        else:
            flash("Erreur SSH inconnue", "error")
        return redirect(url_for("admin_dashboard")) 

    rs.ajoutR(nom, ip, session["idEntreprise"])#mettre mdp <----------------------
    flash("Raspberry ajouté avec succès", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/action_rasp", methods=["POST"])
@reqrole('admin')
def action_rasp():
    button = request.form.get("action")
    rasp_id = request.form.get("raspberry-select")

    if rasp_id is None:
        flash("Aucun Raspberry sélectionné", "error")
        return redirect(url_for("admin_dashboard"))

    rasp = rs.getRasp(rasp_id)

    if not rasp:
        flash("Raspberry introuvable", "error")
        return redirect(url_for("admin_dashboard"))

    nom = rasp["nomLecteur"]
    ip = rasp["ip"]
    print("rasp_ip :",ip)
    rasp_id = int(rasp_id)

    if not ip:
        message=ts.message_langue("Aucun Raspberry sélectionné","No Raspberry selected")
        flash(message, "error")
        return redirect(url_for("admin_dashboard"))
    
    if button=="delete-rasp":
        rs.supprimeR(rasp_id)
        message=ts.message_langue("Raspberry supprimé avec succès","Raspberry successfully deleted")
        flash(message, "success")

    elif button=="envoie-ping":
        if pingRasp(ip):
            message=ts.message_langue("Ping et initialisation OK","Ping and initialisation OK")
            flash(message, "success")
        else:
            message=ts.message_langue("Erreur lors de l'initialisation","Error during initialisation")
            flash(message, "error")
        
    #tmp
    elif button == "test":
        if envoieChangementPlanning(nom, ip):
            flash("Envoi du planning OK", "success")
        else:
            flash("Pas de Raspberry trouvé", "error")

        
    return redirect(url_for("admin_dashboard"))

def envoieChangementPlanning(nom, ip):
    if not ip:
        return False
    subprocess.run(["rsync", "-avz", "--delete", "-e", "ssh","./app/static/rasdata/",  f"{nom}@{ip}:/home/{nom}/musiquali/"])
    print("fini envoie")
    time.sleep(5)
    print("lancement RAS.py")
    print(f"ssh {nom}@{ip} python3 /home/{nom}/musiquali/RAS.py")
    subprocess.Popen(["ssh", "-tt", f"{nom}@{ip}", "python3", "-u", f"/home/{nom}/musiquali/RAS.py"])
    # subprocess.Popen([
    #             "ssh",
    #             f"{nom}@{ip}",
    #             "nohup python3 -u /home/{nom}/musiquali/RAS.py > /home/{nom}/musiquali/ras.log 2>&1 &"
    #         ])
    print("fini RAS.py")


last_sync = {}  # mémorise le dernier rsync par raspberry
def recupLogs(idLecteur, nom, ip):
    dest = Path(f"./app/static/raspLogs/{nom}/logs/")
    dest.mkdir(parents=True, exist_ok=True)
    log = subprocess.run(["rsync", "-avz", "-e", "ssh", f"{nom}@{ip}:/home/{nom}/musiquali/logs/", str(dest)])
    
    #met en base de données les fichiers récupérer
    for file in dest.iterdir():
        if file.is_file():
            ls.add_log(idLecteur, file.name)
    return log

def pingRasp(ip):
    result = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
    return result.returncode == 0
        
dernierOk = {}
etatPing = {}
def pingLoop():
    print("PING LOOP DEMARRE")
    while True:
        raspberrys = rs.montreToutRasp()
        for r in raspberrys:
            if r.ip is None or r.nomLecteur is None:
                continue  # Ignorer les entrées avec des informations incomplètes
            ok = pingRasp(r.ip)
            if ok : 
                print(f"ok pour {r.nomLecteur} ({r.ip})")
                etatPing[r.nomLecteur] = True
                dernierOk[r.nomLecteur] = time.strftime('%Y-%m-%d %H:%M:%S')

                # rajout logs(1 fois toutes les 5 minutes max)
                now = time.time()
                last = last_sync.get(r.nomLecteur, 0)

                if now - last > 300:  # 300s = 5 min
                    envoieChangementPlanning(r.nomLecteur, r.ip)

                    print(f"sync logs pour {r.nomLecteur}")
                    recupLogs(r.idLecteur, r.nomLecteur, r.ip)
                    last_sync[r.nomLecteur] = now

            else:
                print(f"pas ok pour {r.nomLecteur} ({r.ip})")
                etatPing[r.nomLecteur] = False
            dernier = dernierOk.get(r.nomLecteur, "Jamais")   
            print(f"Dernier ping : {dernier}")
        time.sleep(30) # 5min

import threading

threading.Thread(
    target=pingLoop,
    daemon=True
).start()#-> déplacement dans services/RaspberryService.py


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