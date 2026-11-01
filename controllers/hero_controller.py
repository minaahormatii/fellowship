from flask import jsonify, request

from db import db
from models.race import Races
from models.realm import Realms
from models.quest import Quests, quest_schema, quests_schema
from models.hero import Heros, hero_schema, heros_schema
from util.reflection import populate_object


def add_hero():
    post_data = request.form if request.form else request.json

    new_hero = Heros.new_hero_obj()
    populate_object(new_hero, post_data)

    db.session.add(new_hero)
    db.session.commit()

    return jsonify({"message": "hero created", "result": hero_schema.dump(new_hero)}), 201

def create_hero_quest():
    post_data = request.form if request.form else request.json

    hero_id = post_data.get("hero_id")
    quest_id = post_data.get("quest_id")

    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if hero_query and quest_query:
        hero_query.quests.append(quest_query)
        db.session.commit()

    return jsonify({"message": "quest added to hero", "result": hero_schema.dump(hero_query)}), 200

def get_all_heros():
    heros_query = db.session.query(Heros).all()

    return jsonify({"message": "heros found", "results": heros_schema.dump(heros_query)}), 200

def get_alive_heros():
    heros_query = db.session.query(Heros).filter(Heros.is_alive == True).all()

    return jsonify({"message": "alive heros found", "results": heros_schema.dump(heros_query)}), 200

def update_hero_by_id(hero_id):
    post_data = request.form if request.form else request.json
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if hero_query:
        populate_object(hero_query, post_data)

        db.session.commit()
        return jsonify({"message": "hero updated", "result": hero_schema.dump(hero_query)}), 200

    return jsonify({"message": "hero not found"}), 404

def get_hero_by_id(hero_id):
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if not hero_query:
        return jsonify({"message": "hero not found"}), 404

    return jsonify({"message": "hero found", "result": hero_schema.dump(hero_query)}), 200

def delete_hero_by_id(hero_id):
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if not hero_query:
        return jsonify({"message": "hero does not exist"}), 404

    try:
        db.session.delete(hero_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete hero"}), 400

    return jsonify({"message": "hero deleted"}), 200

def get_quests_by_hero_id(hero_id):
    hero_query = db.session.query(Heros).filter(
        Heros.hero_id == hero_id
    ).first()

    if not hero_query:
        return jsonify({"message": "hero not found"}), 404

    return jsonify({
        "message": "quests found",
        "results": quests_schema.dump(hero_query.quests)
    }), 200



  
