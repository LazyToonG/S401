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
    

    rasps = rs.montreToutRaspGlobal()
    if any(r.ip == ip for r in rasps):
        message=ts.message_langue("Raspberry déjà existant","Raspberry already exists")
        flash(message,"error")
        return redirect(url_for("admin_dashboard"))
    
    try:
        try:
            print(f"Vérification de l'IP : {ip}")
            ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError:
            message=ts.message_langue("IP invalide","Invalid IP address")
            flash(message, "error")
            return redirect(url_for("admin_dashboard"))
        # subprocess.run(["scp", "-r", "./app/static/rasdata/*", f"{nom}@{ip}:/home/{nom}/musiquali/"])
        # print(f"sshpass -p {mdp} ssh-copy-id -o StrictHostKeyChecking=no {nom}@{ip}")
        subprocess.run(["sshpass", "-p", mdp, "ssh-copy-id", "-o", "StrictHostKeyChecking=no", f"{nom}@{ip}"], check=True, timeout=8, capture_output=True, text=True)

    except subprocess.TimeoutExpired:
        message=ts.message_langue("Délai dépassé : le Raspberry ne répond pas","Timeout: the Raspberry is not responding")
        flash(message, "error")
        return redirect(url_for("admin_dashboard"))
    
    except subprocess.CalledProcessError as e:
        error = (e.stderr or "").lower()

        if "permission denied" in error:
            message=ts.message_langue("Mot de passe SSH incorrect","Incorrect SSH password")
            flash(message, "error")
        elif "connection refused" in error:
            message=ts.message_langue("Connexion refusée (SSH off ?)","Connection refused (SSH disabled?)")
            flash(message, "error")
        elif "no route to host" in error:
            message=ts.message_langue("Raspberry inaccessible","Raspberry is unreachable")
            flash(message, "error")
        else:
            message=ts.message_langue("Erreur : SSH inconnue","Error: Unknown SSH")
            flash(message, "error")
        return redirect(url_for("admin_dashboard")) 

    rs.ajoutR(nom, ip, session["idEntreprise"])#mettre mdp <----------------------
    message=ts.message_langue("Raspberry ajouté avec succès","Raspberry successfully added")
    flash(message, "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/action_rasp", methods=["POST"])
@reqrole('admin')
def action_rasp():
    button = request.form.get("action")
    rasp_id = request.form.get("raspberry-select")

    if rasp_id is None:
        message=ts.message_langue("Aucun Raspberry sélectionné","No Raspberry selected")
        flash(message, "error")
        return redirect(url_for("admin_dashboard"))

    rasp = rs.getRasp(rasp_id)

    if not rasp:
        message=ts.message_langue("Raspberry introuvable","Raspberry not found")
        flash(message, "error")
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
            message=ts.message_langue("Envoi du planning OK","Schedule sent – OK")
            flash(message, "success")
        else:
            message=ts.message_langue("Pas de Raspberry trouvé","No Raspberry found")
            flash(message, "error")

        
    return redirect(url_for("admin_dashboard"))


def envoieChangementPlanning(nom, ip):
    """
    Envoie le contenu de ./app/static/newData/ vers le Raspberry distant via rsync,
    puis lance RAS.py sur le Raspberry via SSH.
    Retourne True si le rsync et le lancement SSH ont réussi, False sinon.
    """

    print(f"Pause de sécurité pour l'écriture du JSON...")
    time.sleep(2)

    if not ip:
        return False

    source = Path(app.static_folder) / "newData"  # <-- chemin absolu

    try:
        print(f"Source rsync : {source}")
        print(f"Existe : {source.exists()}")
        print(f"Contenu : {list(source.iterdir())}")
        subprocess.run(
            # ["rsync", "-avz", "--delete", "-e", "ssh", "./app/static/rasdata/", f"{nom}@{ip}:/home/{nom}/musiquali/"],
            ["rsync", "-avz", "--delete", "--exclude=logs/", "-e", "ssh", str(source) + "/", f"{nom}@{ip}:/home/{nom}/musiquali/"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        print("fini envoie")
    except subprocess.TimeoutExpired:
        print(f"Timeout rsync pour {nom}@{ip}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Erreur rsync pour {nom}@{ip} : {(e.stderr or '').strip()}")
        return False

    time.sleep(5)
    print(f"Arrêt forcé de l'ancienne instance de RAS.py sur {nom}@{ip}")
    # On passe la commande distante sous forme d'une chaîne unique
    subprocess.run(["ssh", f"{nom}@{ip}", "pkill -9 -f RAS.py"], capture_output=True)

    print("lancement RAS.py")
    print(f"ssh {nom}@{ip} python3 /home/{nom}/musiquali/RAS.py")
    try:
        subprocess.Popen(["ssh", "-tt", f"{nom}@{ip}", "python3", "-u", f"/home/{nom}/musiquali/RAS.py"])
    except OSError as e:
        print(f"Erreur lancement RAS.py pour {nom}@{ip} : {e}")
        return False

    print("fini RAS.py")
    return True
    # subprocess.Popen([
    #             "ssh",
    #             f"{nom}@{ip}",
    #             "nohup python3 -u /home/{nom}/musiquali/RAS.py > /home/{nom}/musiquali/ras.log 2>&1 &"
    #         ])

@app.route("/admin/api/force_send_planning", methods=["POST"])
@reqrole('admin', 'commercial')
def force_send_planning():
    global last_sync # Indispensable pour parler avec la boucle automatique
    
    idEntreprise = session.get('idEntreprise')
    raspberrys = rs.montreToutRasp(idEntreprise)
    
    for r in raspberrys:
        if r.ip and r.nomLecteur:
            if pingRasp(r.ip):
                print(f"Action Bouton : Envoi MANUEL pour {r.nomLecteur}")
                recupLogs(r.idLecteur, r.nomLecteur, r.ip)
                envoieChangementPlanning(r.nomLecteur, r.ip)
                
                # On remet le chronomètre à zéro pour que l'auto attende 5 min
                last_sync[r.nomLecteur] = time.time()
            else:
                print(f"Échec : {r.nomLecteur} est hors ligne.")
                
    return {"status": "success", "message": "Planning déployé !"}

last_sync = {}  # mémorise le dernier rsync par raspberry
def recupLogs(idLecteur, nom, ip):
    # En ciblant directement le dossier parent, rsync va fusionner le contenu
    dest = Path(app.static_folder) / "raspLogs"
    dest.mkdir(parents=True, exist_ok=True)
    
    # On utilise f"{nom}/" dans la destination pour éviter la création du sous-dossier /logs/
    log = subprocess.run(
        ["rsync", "-avz", "-e", "ssh", 
         f"{nom}@{ip}:/home/{nom}/musiquali/logs/",         # Source distante
         str(dest / nom)],                                   # Destination locale propre
        capture_output=True, text=True
    )
    
    # On parcourt le dossier propre de la Raspberry
    rasp_dir = dest / nom
    if rasp_dir.exists():
        for file in rasp_dir.iterdir():
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
        raspberrys = rs.montreToutRaspGlobal()
        for r in raspberrys:
            if r.ip is None or r.nomLecteur is None:
                continue  # Ignorer les entrées avec des informations incomplètes

            try:
                ok = pingRasp(r.ip)
            except Exception as e:
                print(f"Erreur ping pour {r.nomLecteur} ({r.ip}) : {e}")
                ok = False

            if ok :
                print(f"ok pour {r.nomLecteur} ({r.ip})")
                etatPing[r.nomLecteur] = True
                dernierOk[r.nomLecteur] = time.strftime('%Y-%m-%d %H:%M:%S')

                # rajout logs(1 fois toutes les 5 minutes max)
                now = time.time()
                last = last_sync.get(r.nomLecteur, 0)

                if now - last > 300:  # 300s = 5 min
                    try:
                        sync_ok = envoieChangementPlanning(r.nomLecteur, r.ip)
                    except Exception as e:
                        print(f"Erreur inattendue lors de l'envoi du planning pour {r.nomLecteur} : {e}")
                        sync_ok = False

                    if sync_ok:
                        print(f"sync logs pour {r.nomLecteur}")
                        try:
                            recupLogs(r.idLecteur, r.nomLecteur, r.ip)
                            last_sync[r.nomLecteur] = now
                        except Exception as e:
                            print(f"Erreur récupération logs pour {r.nomLecteur} : {e}")
                    else:
                        print(f"échec de l'envoi du planning pour {r.nomLecteur}, nouvelle tentative au prochain cycle")

            else:
                print(f"pas ok pour {r.nomLecteur} ({r.ip})")
                etatPing[r.nomLecteur] = False
            dernier = dernierOk.get(r.nomLecteur, "Jamais")   
            print(f"Dernier ping : {dernier}")
        time.sleep(30) # 300 -> 5min

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