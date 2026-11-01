from flask import Blueprint

import controllers

quest = Blueprint('quest', __name__)

@quest.route("/quest", methods=["POST"])
def add_quest():
    return controllers.add_quest()

@quest.route("/quest/<quest_id>", methods=["GET"])
def get_quest_by_id(quest_id):
    return controllers.get_quest_by_id(quest_id)

@quest.route("/quests/<difficulty>", methods=["GET"])
def get_quests_by_difficulty(difficulty):
    return controllers.get_quests_by_difficulty(difficulty)

@quest.route("/quests/<hero_id>", methods=["GET"])
def get_quests_by_hero(hero_id):
    return controllers.get_quests_by_hero(hero_id)

@quest.route("/quest/<quest_id>", methods=["PUT"])
def update_quest_by_id(quest_id):
    return controllers.update_quest_by_id(quest_id)

@quest.route("/quest/<quest_id>", methods=["PUT"])
def complete_quest_by_id(quest_id):
    return controllers.complete_quest_by_id(quest_id)

@quest.route("/quest/delete/<quest_id>", methods=["DELETE"])
def delete_quest_by_id(quest_id):
    return controllers.delete_quest_by_id(quest_id)