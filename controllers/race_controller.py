from flask import jsonify, request

from db import db
from models.race import Races, race_schema, races_schema
from util.reflection import populate_object


def add_race():
    post_data = request.form if request.form else request.json

    new_race = Races.new_race_obj()
    populate_object(new_race, post_data)

    db.session.add(new_race)
    db.session.commit()


    return jsonify({"message": "race created", "result": race_schema.dump(new_race)}), 201

def get_all_races():
    race_query = db.session.query(Races).all()

    return jsonify({"message": "races found", "results": races_schema.dump(race_query)}), 200

def update_race_by_id(race_id):
    post_data = request.form if request.form else request.json
    race_query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if race_query:
        populate_object(race_query, post_data)

        db.session.commit()
        return jsonify({"message": "race updated", "result": race_schema.dump(race_query)}), 200

    return jsonify({"message": "race not found"}), 404

def get_race_by_id(race_id):
    race_query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not race_query:
        return jsonify({"message": "race not found"}), 404

    return jsonify({"message": "race found", "result": race_schema.dump(race_query)}), 200

def delete_race_by_id(race_id):
    race_query = db.session.query(Races).filter(Races.race_id == race_id).first()


    if not race_query:
        return jsonify({"message": f"race does not exist"}), 404

    try:
        db.session.delete(race_query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete race"}), 400

    return jsonify({"message": "race deleted"}), 200