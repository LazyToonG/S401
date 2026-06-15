from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.LoginController import reqrole
from app.services.TraductionService import Traductionservice
from app.services.marketingService import MarketingService
from app import app

marketingService = MarketingService()


@app.route("/marketing")
@reqrole("admin","marketing")
def marketing():
    data = marketingService.get_marketing_data()
    return render_template(
        "marketing.html",
        playlists=data["playlists"],
        musiques=data["musiques"],
        musics=data["musics"],
    )


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


@app.route("/marketing/playlist/<int:playlist_id>/delete", methods=["POST"])
@reqrole("admin","marketing")
def delete_playlist(playlist_id):
    marketingService.delete_playlist(playlist_id)
    return redirect(url_for("marketing"))


@app.route("/marketing/music/<int:music_id>/delete", methods=["POST"])
@reqrole("admin","marketing")
def delete_music(music_id):
    marketingService.delete_music(music_id)
    
    # hop de l'ajax
    #pour ne pas recharger la page a chaque del
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return '', 204

    return redirect(url_for("marketing"))



#je fusionne service musique et service playliste parceque c t debile de les séparer
#enfin peut etre pas mais ils était pas si grands que ca

@app.route("/upload", methods=["POST"])
@reqrole('admin')
def upload_music():
    files = request.files.getlist("audio")

    if not files:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {"error": "Aucun fichier sélectionné"}, 400
        flash("Aucun fichier sélectionné", "error")
        return redirect(url_for("marketing"))

    created = marketingService.save_music_files(files)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # async
        return {
            "musiques": [
                {"idMusique": m.idMusique, "nomMusique": m.nomMusique, "duree": m.duree}
                for m in created
            ]
        }

    flash("Musique(s) ajoutée(s) avec succès", "success")
    return redirect(url_for("marketing"))

# marketingController.py
