from flask import jsonify, request

from db import db
from models.realm import Realms, realm_schema, realms_schema
from util.reflection import populate_object


def add_realm():
    post_data = request.form if request.form else request.get_json()

    new_realm = Realms.new_realm_obj()
    populate_object(new_realm, post_data)

    db.session.add(new_realm)
    db.session.commit()

    return jsonify({"message": "realm created", "result": realm_schema.dump(new_realm)}), 201

def get_all_realms():
    realm_query = db.session.query(Realms).all()

    return jsonify({"message": "realms found", "results": realms_schema.dump(realm_query)}), 200

def update_realm_by_id(realm_id):
    post_data = request.form if request.form else request.get_json()
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if realm_query:
        populate_object(realm_query, post_data)

        db.session.commit()
        return jsonify({"message": "realm updated", "result": realm_schema.dump(realm_query)}), 200
    
    return jsonify({"message": "company not found"}), 404

def get_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not realm_query:
        return jsonify({"message": "realm not found"}), 404

    return jsonify({"message": "realm found", "result": realm_schema.dump(realm_query)}), 200

def delete_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    

    if not realm_query:
        return jsonify({"message": "realm not found"}), 404

    try:
        db.session.delete(realm_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete realm"}), 400

    return jsonify({"message": "realm deleted"}), 200