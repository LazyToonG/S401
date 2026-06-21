from flask import request, jsonify, render_template
from app import app
from app.services.PlanningService import PlanningService

planningService = PlanningService()


@app.route("/commercial", methods=["GET"])
def commercial_page():
    """Sert la page planning.html (calendriers commerciaux + messages)."""
    return render_template("planning.html")


def _to_dict(planning):
    return {
        "idPlanning": planning.idPlanning,
        "idPlaylist": planning.idPlaylist,
        "idMSG": planning.idMSG,
        "StartTime": planning.StartTime,
        "idEntreprise": planning.idEntreprise
    }


@app.route("/planning/data", methods=["GET"])
def get_planning_data():
    """Retourne tout le planning (les deux calendriers) pour reconstruire l'état au chargement."""
    idEntreprise = request.args.get("idEntreprise", 1, type=int)
    planning = planningService.get_all(idEntreprise)
    return jsonify([_to_dict(p) for p in planning])


@app.route("/planning/save", methods=["POST"])
def save_planning():
    """
    Reçoit l'état complet des deux calendriers et synchronise la bd
    (insert / update / delete par diff).

    Payload JSON attendu:
    {
        "idEntreprise": 1,
        "boxes": [
            {"idPlanning": 12, "idPlaylist": 3, "idMSG": null, "StartTime": "2026-06-22T08:30:00"},
            {"idPlanning": null, "idPlaylist": null, "idMSG": 7, "StartTime": "2026-06-23T09:00:00"},
            ...
        ]
    }
    """
    data = request.get_json(silent=True) or {}
    boxes = data.get("boxes", [])
    idEntreprise = data.get("idEntreprise", 1)

    try:
        results = planningService.sync(boxes, idEntreprise)
        planningService.export_planning(idEntreprise)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify([_to_dict(p) for p in results])


@app.route("/planning/<int:planning_id>", methods=["DELETE"])
def delete_planning(planning_id):
    """Supprime une entrée précise du planning."""
    planningService.delete(planning_id)
    return jsonify({"success": True})