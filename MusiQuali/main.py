from app import app

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True, use_reloader=False)  # use_reloader=False pour éviter le double lancement du script