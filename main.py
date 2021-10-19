import json
from flask import Flask, Response, request
import os

app = Flask(__name__)
json_file_path = "/Users/banestamenic/PycharmProjects/pythonProject/users.json"


class UserNotFoundException(Exception):
    pass


class DB:
    def __init__(self):
        pass

    @classmethod
    def get_users(cls):
        file_path = "./users.json"
        if os.stat(file_path).st_size == 0:
            return None
        else:
            with open('users.json', 'r') as f:
                data = json.loads(f.read())
                return data['users']

    @classmethod
    def get_user(cls, user_id):
        with open('users.json', 'r') as f:
            data = json.loads(f.read())
            if user_id in data['users'].keys():
                return data['users'][user_id]
            else:
                raise UserNotFoundException

    @classmethod
    def insert_user(cls, new_user):
        with open('users.json', 'r') as f:
            data = json.loads(f.read())
            max_id = max(int(x) for x in data['users'].keys()) # int(max(data['users'].keys()))
            if not max_id:
                max_id = 0

        data['users'][str(max_id + 1)] = new_user

        with open('users.json', 'w') as out:
            out.write(json.dumps(data))

    @classmethod
    def update_user(cls, user_id, user):
        file_path = "./users.json"
        if os.stat(file_path).st_size == 0:
            return None

        with open('users.json', 'r') as f:
            data = json.loads(f.read())
        keys = data['users'].keys()
        if user_id in keys:
            data['users'][user_id] = user
            with open('users.json', 'w') as out:
                json.dump(data, out)
        else:
            raise UserNotFoundException

    @classmethod
    def delete_user(cls, user_id):
        with open('users.json', 'r') as f:
            data = json.loads(f.read())
        if user_id in data['users']:
            deleted_user = data['users'].pop(user_id)
            with open('users.json', 'w') as out:
                json.dump(data, out)
                return deleted_user
        else:
            raise UserNotFoundException


@app.route('/users/', methods=['GET'])
def get_users():
    try:
        users = DB.get_users()
        return Response(json.dumps(users), status=200, mimetype='application/json')
    except UserNotFoundException:
        return Response("Empty", status=404, mimetype='application/json')


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = DB.get_user(user_id)
        return Response(json.dumps(user), status=200, mimetype='application/json')
    except UserNotFoundException:
        return Response("User not found", status=404, mimetype='application/json')


@app.route('/users/', methods=['POST'])
def insert_user():
    user = json.loads(request.data)
    try:
        return Response(json.dumps(user), status=201, mimetype='application/json')
    except UserNotFoundException:
        return Response("Email exists", status=400, mimetype='application/json')


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = json.loads(request.data)
    try:
        DB.update_user(user_id, user)
        return Response(json.dumps(DB.get_users()), status=200, mimetype='application/json')
    except UserNotFoundException:
        return Response("User does not exist", status=404, mimetype='application/json')


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        deleted_user = DB.delete_user(user_id)
        return Response(json.dumps(deleted_user), status=204, mimetype='application/json')
    except UserNotFoundException:
        return Response("User does not exist", status=404, mimetype='application/json')


# if __name__ == '__main__':
# test_try()
