from flask import jsonify, request

from db import db
from models.race import Races
from models.realm import Realms
from models.hero import Heros
from models.quest import Quests, quest_schema, quests_schema
from util.reflection import populate_object


def add_quest():
    post_data = request.form if request.form else request.get_json()

    new_quest = Quests.new_quest_obj()
    populate_object(new_quest, post_data)

    db.session.add(new_quest)
    db.session.commit()

    return jsonify({"message": "quest created", "result": quest_schema.dump(new_quest)}), 201

def get_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify({"message": "quest not found"}), 404

    return jsonify({"message": "quest found", "result": quest_schema.dump(quest_query)}), 200

def get_quests_by_difficulty(difficulty):
    quest_query = db.session.query(Quests).filter(Quests.difficulty == difficulty).all()

    if not quest_query:
        return jsonify({"message": "quest not found"}), 404

    return jsonify({"message": "quests found", "results": quests_schema.dump(quest_query)}), 200

def get_quests_by_hero(hero_id):
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if not hero_query:
        return jsonify({"message": "hero not found"}), 404

    quests = hero_query.quests

    return jsonify({"message": "quests found", "results": quests_schema.dump(quests)}), 200

def update_quest_by_id(quest_id):
    post_data = request.form if request.form else request.get_json()
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if quest_query:
        populate_object(quest_query, post_data)

        db.session.commit()
        return jsonify({"message": "quest updated", "result": quest_schema.dump(quest_query)}), 200

    return jsonify({"message": "quest not found"}), 404

def complete_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify({"message": "quest not found"}), 404

    quest_query.is_completed = True
    db.session.commit()

    return jsonify({"message": "quest completed", "result": quest_schema.dump(quest_query)}), 200

def delete_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify({"message": "quest does not exist"}), 404

    try:
        db.session.delete(quest_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete quest"}), 400

    return jsonify({"message": "quest deleted"}), 200
