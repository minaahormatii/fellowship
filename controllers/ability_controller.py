from flask import jsonify, request

from db import db
from models.ability import Abilities, ability_schema, abilities_schema
from util.reflection import populate_object


def add_ability():
    post_data = request.form if request.form else request.json

    new_ability = Abilities.new_ability_obj()
    populate_object(new_ability, post_data)

    db.session.add(new_ability)
    db.session.commit()

    return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201

def get_ability_by_id(ability_id):
    ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not ability_query:
        return jsonify({"message": "ability not found"}), 404

    return jsonify({"message": "ability found", "result": ability_schema.dump(ability_query)}), 200

def update_ability_by_id(ability_id):
    post_data = request.form if request.form else request.json
    ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if ability_query:
        populate_object(ability_query, post_data)

        db.session.commit()
        return jsonify({"message": "ability updated", "result": ability_schema.dump(ability_query)}), 200

    return jsonify({"message": "ability not found"}), 404

def delete_ability_by_id(ability_id):
    ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not ability_query:
        return jsonify({"message": "ability not found"}), 404

    try:
        db.session.delete(ability_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete ability"}), 400

    return jsonify({"message": "ability deleted"}), 200