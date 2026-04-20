# app/controllers/MarketingController.py
from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.controllers.LoginController import reqrole
from app.services.MusiqueService import MusiqueService
from app.services.playlistServiceMarketing import PlaylistService
from app.services.TraductionService import Traductionservice

ts = Traductionservice()
service = MusiqueService()
playlist_service = PlaylistService()

@app.route('/marketing', methods=['GET', 'POST'])
@reqrole("admin","marketing","commercial")
def marketing():
    # Translations
    traductions = ts.tradMarketing()
    langue_choisie = ts.getLangue()
    textes = traductions[langue_choisie]

    # Page content
    playlists = playlist_service.get_all()
    sort = request.args.get("sort", "date")
    musiques = service.get_musiques(sort)#on s'en sert pas je crois
    user = session['username']
    role = session['role']
    metadata = {"title": "Espace Marketing", "pagename": "marketing"}

    # Restrict commercial users to "message" playlist only
    if role == "commercial":
        # For commercial, filter playlists to only show "message"
        playlists = [p for p in playlists if p.title.lower() == "message"]
        if not playlists:
            message=ts.message_langue("Accès refusé: la playlist 'message' n'existe pas","Access denied: the 'message' playlist does not exist.")
            flash(message, "error")
            return render_template("marketing_v2.html",metadata=metadata,sort=sort,current_lang=langue_choisie,musiques=musiques,t=textes,playlists=playlists,user=user,role=role,musics=musics,selected_playlist_id=selected_playlist_id)

    # Playlist selection
    selected_playlist_id = None
    musics = []

    if request.method == "POST":
        playlist_id_raw = request.form.get("playlist_id")
        if playlist_id_raw:
            # For commercial users, verify they only access "message" playlist
            if role == "commercial":
                selected_playlist = playlist_service.get_by_id(playlist_id_raw)
                if not selected_playlist or selected_playlist.title.lower() != "message":
                    message=ts.message_langue("Accès refusé: vous ne pouvez modifier que la playlist 'message'","Access denied: you can only edit the 'message' playlist.")
                    flash(message,"error")
                    return render_template("marketing_v2.html",metadata=metadata,sort=sort,current_lang=langue_choisie,musiques=musiques,t=textes,playlists=playlists,user=user,role=role,musics=musics,selected_playlist_id=selected_playlist_id)
            
            #si une playlist est selectionnée
            selected_playlist_id = str(playlist_id_raw)  
            a = playlist_service.musics_in_playlist(selected_playlist_id)
            for music in a:
                musics.append(music.title)

    return render_template(
        "marketing_v2.html",
        metadata=metadata,
        sort=sort,
        current_lang=langue_choisie,
        musiques=musiques,
        t=textes,
        playlists=playlists,
        user=user,
        role=role,
        musics=musics,
        selected_playlist_id=selected_playlist_id
    )



@app.route("/delete/<int:id>")
def delete(id):
    service.delete_musique(id)
    return redirect(url_for("marketing"))

@app.route("/search_by_title")
def search_by_title():
    traductions=ts.tradMarketing()
    langue_url = request.args.get('lang')
        
    langue_choisie=ts.getLangue()
    textes = traductions[langue_choisie]
    user = session['username']
    role = session['role']

    title = request.args.get("title")
    musiques = service.search_by_title(title)#nexiste pas
    if musiques:
        return render_template("marketing_v2.html", musiques=[musiques], t=textes, current_lang=langue_choisie, user=user, role=role)
    return redirect(url_for("marketing"))

@app.route("/playlist/create", methods=["POST"])
@reqrole("admin","marketing")
def create_playlist():
    title = request.form.get("title")
    if not title:
        message=ts.message_langue("Title de playlist obligatoire","Required playlist title")
        flash(message,"error")
        return redirect(url_for("marketing"))

    playlist_service.create_playlist(title=title)
    message=ts.message_langue("Playlist créée avec succès","Playlist successfully created")
    flash(message,"success")
    return redirect(url_for("marketing"))

@app.route("/playlist/delete", methods=["POST"])
@reqrole("admin","marketing")
def delete_playlist():
    
    playlist_id = request.form.get("playlist_id")  # récupère l'id du formulaire
    if not playlist_id:
        message=ts.message_langue("Aucune playlist sélectionnée","No playlist selected")
        flash(message,"error")
        return redirect(url_for('marketing'))
    
    a=playlist_service.musics_in_playlist(playlist_id)
    for music in a:
        if music is not None:
            service.delete_musique(music)
    playlist_service.delete_playlist(playlist_id)
    # for music in a:
    #     delSql.append(music.id)
    # for music in a:
    #     delMp3.append(music.path)
    message=ts.message_langue("Playlist supprimée avec succès","Playlist successfully deleted")
    flash(message,"success")
    return redirect(url_for('marketing'))

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("audio")
    playlist_id = request.form.get("playlist_id")
    role = session.get('role')

    if not file or not playlist_id:
        message=ts.message_langue("Fichier ou playlist manquant","File or playlist missing")
        flash(message,"error")
        return redirect(url_for("marketing"))

    playlist = playlist_service.get_by_id(int(playlist_id))
    if not playlist:
        message=ts.message_langue("Playlist invalide","Invalid playlist")
        flash(message,"error")
        return redirect(url_for("marketing"))
    
    # Verify commercial users can only upload to "message" playlist
    if role == "commercial" and playlist.title.lower() != "message":
        message=ts.message_langue("Accès refusé: vous ne pouvez modifier que la playlist 'message'","Access denied: you can only edit the 'message' playlist.")
        flash(message, "error")
        return redirect(url_for("marketing"))

    music = service.save_file(file)
    playlist_service.add_music_to_playlist(playlist.id, music.id)

    message=ts.message_langue("Playlist enregistrée avec succès","Playlist successfully saved")
    flash(message,"success")
    return redirect(url_for("marketing"))

# @app.route("/musicsinplaylist", methods=["GET", "POST"])
# def musicsinplaylist():

#     t = ts.getLangue()

#     playlist_id = request.values.get("playlist_id")

#     playlists = playlist_service.get_all()

#     musics = []
#     if playlist_id:
#         musics = playlist_service.musics_in_playlist(playlist_id)

#     return render_template(
#         "marketing_v2.html",
#         playlists=playlists,
#         musics=musics,
#         selected_playlist_id=playlist_id,
#         t=t
#     )


