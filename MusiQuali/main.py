from app import app

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)  # use_reloader=False pour éviter le double lancement du script

# , ssl_context="adhoc"