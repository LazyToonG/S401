from flask import render_template, request, session, redirect, url_for
from app import app
from app.services.TraductionService import Traductionservice
#from app.controllers.LoginController import reqlogged
from app.services.service_schedule import service_schedule

ts = Traductionservice()


class IndexController:

    @app.route('/', methods=['GET'])
    def index():

        trad = ts.tradIndex()
        langue_choisie = session.get('lang', ts.getLangue())
        textes = trad[langue_choisie]
        metadata = {"title": "Accueil", "pagename": "accueil"}
        return render_template('index.html', metadata=metadata, t=textes, current_lang=langue_choisie)

    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang in ['fr', 'en']:
            session['lang'] = lang
        
        # Sécurité : Si request.referrer est vide ou buggé, on redirige proprement vers l'accueil
        if request.referrer and request.referrer != request.url:
            return redirect(request.referrer)
            
        return redirect(url_for('index'))