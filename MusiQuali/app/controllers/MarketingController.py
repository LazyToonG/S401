from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.controllers.LoginController import reqrole
from app.services.TraductionService import Traductionservice
from app.services.marketingService import MarketingService
from app import app

marketingService = MarketingService()

ts = Traductionservice()




@app.route("/marketing")
def marketing():
    traductions=ts.tradMarketing()

    langue_choisie=ts.getLangue()
    textes = traductions[langue_choisie]
    data = marketingService.get_marketing_data()
    return render_template(
        "marketing.html",
        playlists=data["playlists"],
        musiques=data["musiques"],
        user=session['username'],
        role=session['role'],
        t=textes
    )

# PLAYLISTES

@app.route("/marketing/playlist/<int:playlist_id>/tracks")
@reqrole("admin","marketing")
def playlist_tracks(playlist_id):
    """Renvoie la composition d'une playlist (pour affichage dynamique)."""
    tracks = marketingService.get_playlist_tracks(playlist_id)
    return {
        "tracks": [
            {"idMusique": m.idMusique, "nomMusique": m.nomMusique, "duree": m.duree}
            for m in tracks
        ]
    }


@app.route("/marketing/playlists", methods=["GET"])
@reqrole('admin', 'marketing')
def get_playlists_json():
    """Retourne la liste des playlists en JSON (pour le calendrier des commerciaux)."""
    data = marketingService.get_marketing_data()
    return jsonify([
        {"idPlaylist": p["idPlaylist"], "title": p["title"]}
        for p in data["playlists"]
    ])


@app.route("/marketing/playlist/add", methods=["POST"])
@reqrole('admin', 'marketing')
def add_playlist():
    title = request.form.get("title")
    if not title:
        return redirect(url_for("marketing"))
    marketingService.add_playlist(title)
    return redirect(url_for("marketing"))

@app.route("/marketing/playlist/<int:playlist_id>/delete", methods=["POST"])
@reqrole('admin', 'marketing')
def delete_playlist(playlist_id):
    marketingService.delete_playlist(playlist_id)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204
    return redirect(url_for("marketing"))


@app.route("/marketing/musiques", methods=["GET"])
@reqrole('admin', 'marketing')
def get_musiques_json():
    """
    Retourne la liste des musiques en JSON. Filtre optionnel via ?prefix=MSG_
    (utilisé par le calendrier des messages pour n'afficher que les MSG_*).
    """
    data = marketingService.get_marketing_data()
    musiques = data["musiques"]

    prefix = request.args.get("prefix")
    if prefix:
        musiques = [m for m in musiques if m.nomMusique.startswith(prefix)]

    return jsonify([
        {"idMusique": m.idMusique, "nomMusique": m.nomMusique, "duree": m.duree}
        for m in musiques
    ])


#------ Musiques

@app.route("/marketing/music/<int:music_id>/delete", methods=["POST"])
@reqrole("admin","marketing")
def delete_music(music_id):
    marketingService.delete_music(music_id)
    
    # hop de l'ajax
    #pour ne pas recharger la page a chaque del
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204

    return redirect(url_for("marketing"))


 
@app.route("/upload", methods=["POST"])
@reqrole('admin')
def upload_music():
    files = request.files.getlist("audio")

    if not files:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {"error": "Aucun fichier sélectionné"}, 400
        flash("Aucun fichier sélectionné", "error")
        return redirect(url_for("marketing"))

    created = marketingService.save_music_files(files, session['idEntreprise'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # async
        return {
            "musiques": [
                {"idMusique": m.idMusique, "nomMusique": m.nomMusique, "duree": m.duree}
                for m in created
            ]
        }

    flash("Musique(s) ajoutée(s) avec succès", "success")
    return redirect(url_for("marketing"))




# ------ RELATION PLAYISTE-MUSIQUE ----


@app.route("/marketing/playlist/<int:playlist_id>/add_music/<int:music_id>", methods=["POST"])
@reqrole('admin', 'marketing')
def add_music_to_playlist(playlist_id, music_id):
    position = request.form.get("position", type=int)
    marketingService.add_music_to_playlist(playlist_id, music_id, position)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204
    return redirect(url_for("marketing"))


@app.route("/marketing/playlist/remove_music/<int:id_couple>", methods=["POST"])
@reqrole('admin', 'marketing')
def remove_music_from_playlist(id_couple):
    marketingService.remove_music_from_playlist(id_couple)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204
    return redirect(url_for("marketing"))


@app.route("/marketing/playlist/save_positions", methods=["POST"])
@reqrole('admin', 'marketing')
def save_positions():
    """
    Reçoit une liste JSON [{idCouple, position}, ...]
    et met à jour les positions en BD.
    """
    data = request.get_json()
    if not data:
        return {"error": "Aucune donnée reçue"}, 400
    marketingService.save_positions(data)
    return '', 204
@app.route("/marketing/playlist/<int:playlist_id>/musiques")
@reqrole('admin', 'marketing')
def get_musiques_by_playlist(playlist_id):
    """Retourne les musiques d'une playlist en JSON."""
    musiques = marketingService.get_musiques_by_playlist(playlist_id)
    return jsonify(musiques)