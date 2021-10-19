import json
from flask import Flask
import requests


def test_number_of_users():
    url = "http://localhost:5000/users"
    response = requests.get(url=url)
    response_body = response.json()
    assert response.status_code == 200
    assert int(max(response_body.keys())) == 2


def test_first_user():
    url = "http://localhost:5000/users/1"
    response = requests.get(url=url)
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["name"] == "Pera"
    assert response_body["surname"] == "Peric"
    assert response_body["email"] == "pera@gmail.com"


def test_valid_user_id(user_id):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    response = requests.get(url=url)
    assert response.status_code == 200


def test_user_non_valid_user_id(user_id):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    response = requests.get(url=url)
    assert response.status_code == 404


def test_insert_valid_user(name, surname, email):
    url = "http://localhost:5000/users/"
    new_user = {'name': name, 'surname': surname, 'email': email}
    response = requests.post(url=url, data=json.dumps(new_user))
    assert response.status_code == 201


def test_update_valid_user(user_id, name, surname, email):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    user = {'name': name, 'surname': surname, 'email': email}
    response = requests.put(url=url, data=json.dumps(user))
    assert response.status_code == 200


def test_update_non_valid_user(user_id, name, surname, email):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    user = {'name': name, 'surname': surname, 'email': email}
    response = requests.put(url=url, data=json.dumps(user))
    assert response.status_code == 404


def test_delete_valid_user(user_id):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    response = requests.delete(url=url)
    assert response.status_code == 204


def test_delete_non_valid_user(user_id):
    url = "http://localhost:5000/users/{}".format(str(user_id))
    response = requests.delete(url=url)
    assert response.status_code == 404


if __name__ == "__main__":
    # test_number_of_users()
    # test_first_user()
    # test_valid_user_id(1)
    # test_non_valid_user_id(5)
    # test_insert_valid_user("Mika", "Mikic", "mika@gmail.com")
    # test_delete_valid_user(4)
    # test_delete_non_valid_user(7)
    test_update_non_valid_user(8, "Bane", "Stamenic", "banega@gmail.com")