from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    list_of_url = []
    for d in data:
        list_of_url.append(d["pic_url"])
    return jsonify(list_of_url)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        for d in data:
            if id == d["id"]:
                return d
        return {"message":f"person with id: {id} was not found in the db"},404
    except:
        return {"message":"invalid id"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    resp = request.json
    if not resp:
        return {"Message":"data not defined"}, 422

    pic_url = resp.get("pic_url")
    
    if not pic_url:
        return {"Message":"Picture URL was not defined"},422
    
    pic_id = resp.get("id")

    if not pic_id:
        return {"Message": "ID not defined"}, 422

    for d in data:
        if pic_id == d["id"]:
            return {"Message": f"picture with id {pic_id} already present"}, 302
    try:
        data.append(resp)
        return {"id": pic_id}, 201
    except NameError:
        return {"Message": "data not defined"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    resp = request.json

    if not resp:
        return jsonify({"message": "No data provided in the request"}), 400

    for d in data:
        if id == d["id"]:
            d.update(resp)
            return {"message": f"Picture data with id {id} updated"},200
    return {"message": "picture not found"}, 404




######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for d in data:
        if id == d["id"]:
            data.remove(d)
            return {"Message":"Picture deleted"}, 204
    return {"Message":"picture not found"}, 404