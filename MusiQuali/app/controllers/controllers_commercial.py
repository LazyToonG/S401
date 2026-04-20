from flask import Blueprint, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from app.services.RaspberryService import RaspberryService
from app.services.service_playlist import service_playlist
from app.services.service_schedule import service_schedule
from app import app
from app.controllers.LoginController import reqrole
from app.services.TraductionService import Traductionservice
import os
import json

ts = Traductionservice()
rs = RaspberryService()

class commercial_Controller:

    @app.route('/commercial', methods=['GET'])
    @reqrole("admin", "commercial")
    def voir_planning():
        traductions=ts.tradCommercial()

        langue_choisie=ts.getLangue()
        textes = traductions[langue_choisie]

        user=session['username']
        role=session['role']
        playlists = service_playlist.get_playlists_api_data()
        return render_template('planning.html', planning=service_schedule.get_planning(), playlists=playlists, t=textes, current_lang=langue_choisie, user=user, role=role)


    @app.route('/admin')
    @reqrole("admin")
    def admin_page():
        traductions=ts.tradAdmin()

        langue_choisie=ts.getLangue()
        textes = traductions[langue_choisie]

        user=session['username']
        role=session['role']
        playlists = service_playlist.get_all_playlists()

        rasp = rs.montreToutRasp()

        return render_template('admin.html', raspberry=rasp, playlists=playlists, t=textes, current_lang=langue_choisie, user=user, role=role)

    @app.route('/add_playlist', methods=['POST'])
    def add_playlist():
        name = request.form.get('name')
        if name:
            service_playlist.create_playlist(name)
            flash(f"Playlist '{name}' créée avec succès.")
        return redirect(url_for('main.admin_page'))

    # @app.route('/add_music', methods=['POST'])
    # def add_music():
    #     playlist_id = request.form.get('playlist_id')
    #     title = request.form.get('title')
    #     artist = request.form.get('artist')
    #     duration = request.form.get('duration')
    #     path = request.form.get('path')

    #     if playlist_id and title and duration:
    #         # service_music n'est pas disponible ici pour le moment
    #         # service_music.add_music(playlist_id, title, artist, duration, path)
    #         flash(f"Musique '{title}' ajoutée avec succès.")
    #     else:
    #         flash("Erreur : Champs manquants.")
    #     return redirect(url_for('main.admin_page'))

    @app.route('/api/playlists')
    def get_playlists():
        data = service_playlist.get_playlists_api_data()
        return jsonify(data)

    @app.route('/move', methods=['POST'])
    def move_music():
        data = request.json
        service_schedule.move_task(
            data['from_day'],
            int(data['from_index']),
            data['to_day'],
            int(data['to_index'])
        )
        return jsonify(success=True)

    @app.route('/sync_day', methods=['POST'])
    def sync_day():
        data = request.get_json(silent=True)
        if not data:
            return jsonify(success=False, error="Données JSON invalides"), 400

        day = data.get('day')
        tasks = data.get('tasks', [])
        start_time = data.get('start_time', '00:00')

        try:
            service_schedule.sync_day(day, tasks, start_time)
            return jsonify(success=True)
        except Exception as e:
            print(f"Erreur sync_day: {e}")
            return jsonify(success=False, error=str(e)), 500

    @app.route('/save_export', methods=['POST'])
    def save_export():
        try:
            # Obtenir le contenu du planning en JSON
            mem_file = service_schedule.export_planning()
            json_content = mem_file.getvalue().decode('utf-8')
            
            # Chemin du dossier static/data en utilisant app.static_folder
            data_dir = os.path.join(app.static_folder, 'rasdata')
            
            # Créer le dossier s'il n'existe pas
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Sauvegarder le fichier JSON
            file_path = os.path.join(data_dir, 'planning_export.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_content)

            rs.envoieChaqueChangementPlanning()
            
            return jsonify(success=True, message="Planning exporté avec succès dans static/data/planning_export.json")
        except Exception as e:
            return jsonify(success=False, message=f"Erreur technique lors de l'exportation : {str(e)}"), 500