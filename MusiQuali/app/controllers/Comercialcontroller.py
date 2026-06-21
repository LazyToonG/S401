from flask import request, jsonify, render_template
from app import app
from app.services.Commercialservice import CommercialService

commercial_service = CommercialService()


@app.route("/commercial", methods=["GET"])
def commercial_page():
    """Sert la page planning.html (gestion des commerciaux)."""
    return render_template("planning.html")


def _to_dict(commercial):
    """
   créer objet json
    """
    return {
        "idCommercial": commercial.idPlaylist,
        "title": commercial.title,
        "idUtilisateur": commercial.idUtilisateur,
        "idPlanning": commercial.idPlanning
    }


@app.route("/commerciaux", methods=["GET"])
def get_commerciaux():
    """Retourne la liste de tous les commerciaux (pour remplir la modal)."""
    commerciaux = commercial_service.get_all_commercials()
    return jsonify([_to_dict(c) for c in commerciaux])


@app.route("/commerciaux/<int:commercial_id>", methods=["GET"])
def get_commercial(commercial_id):
    """Retourne un commercial précis."""
    commercial = commercial_service.get_commercial(commercial_id)
    if commercial is None:
        return jsonify({"error": "Commercial introuvable"}), 404

    return jsonify(_to_dict(commercial))


@app.route("/commerciaux", methods=["POST"])
def create_commercial():
    """Crée un nouveau commercial."""
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    idUtilisateur = data.get("idUtilisateur", 1)
    idPlanning = data.get("idPlanning", 1)

    try:
        commercial = commercial_service.create_commercial(
            title=title,
            idUtilisateur=idUtilisateur,
            idPlanning=idPlanning
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(_to_dict(commercial)), 201


@app.route("/commerciaux/<int:commercial_id>", methods=["PUT"])
def rename_commercial(commercial_id):
    """Renomme un commercial existant."""
    data = request.get_json(silent=True) or {}
    new_title = data.get("title")

    try:
        commercial = commercial_service.rename_commercial(commercial_id, new_title)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(_to_dict(commercial))


@app.route("/commerciaux/<int:commercial_id>", methods=["DELETE"])
def delete_commercial(commercial_id):
    """Supprime un commercial."""
    try:
        commercial_service.delete_commercial(commercial_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"success": True})