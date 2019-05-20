import sys
import os
import json, imp, ast
import configparser
from functools import wraps
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient

import flask_restplus

from flask import Blueprint, request, abort, Response, jsonify, url_for, session
from flask import current_app as app
from flask_restplus import Api, Resource, fields, reqparse


DEBUG = True

blueprint = Blueprint('userinfo',__name__,url_prefix='/api/userinfo')
api = Api(blueprint)
ns = api.namespace('userinfo',description='Simple Flask Ldap App')


add_user_model = api.model("add_user_model", {
    "firstName": fields.String("firstName"),
    "lastName": fields.String("lastName"),
    "dob": fields.String("dob"),
    "email": fields.String("email"),
    "country": fields.String("country"),
    "passwordHash": fields.String("passwordHash")
})

client = MongoClient('localhost',27017)
db = client.test
collection = db.registration

utils = imp.load_source('*', './userinfo/utils.py')


@ns.route("")
@ns.route("/<id>")
class Home(Resource):
    # method_decorators=[must_auth]
    def get(self):
        """
        Function to get the userinfos.
        """
        try:
            q_params = utils.parse_q_params(request.query_string)
            if q_params:
                query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in q_params.items()}
                records_fetched = collection.find(query)
                if records_fetched.count() > 0:
                    return json_util.dumps(records_fetched)
                else:
                    return "No Records found", 404
            else:
                if collection.find().count > 0:
                    return Response(dumps(collection.find()), mimetype='application/json')
                else:
                    return jsonify([])
        except:
            raise #return "", 500

    @api.expect(add_user_model)    
    def post(self):
        """
        Function to add new userinfo(s).
        """
        try:
            try:
                body = ast.literal_eval(json.dumps(request.get_json()))
            except:
                return "", 400

            record_created = collection.insert(body)

            if isinstance(record_created, list):
                return jsonify({'ids' : [str(v) for v in record_created]}), 201
            else:
                return jsonify({ 'id' : str(record_created)}), 201
        except:
            raise #return "", 500

    @api.expect(add_user_model)    
    def put(self, id=None):
        """
        Function to update a userinfo.
        """
        try:
            try:
                body = ast.literal_eval(json.dumps(request.get_json()))
            except:
                return "", 400
            records_updated = collection.update_one({"_id": ObjectId(id)}, body)

            if records_updated.modified_count > 0:
                return "Updated {} items!".format(records_updated.modified_count), 200
            else:
                return "", 404
        except:
            raise #return "", 500

    
    def delete(self, id=None):
        """
        Function to delete a userinfo.
        """
        try:
            q_params = utils.parse_q_params(request.query_string)
            delete_user = collection.delete_one({"_id": ObjectId(id)})
            if delete_user.deleted_count > 0 :
                return "Deleted {} items!".format(delete_user.deleted_count), 204
            else:
                return "", 404
        except:
            raise #return "", 500


