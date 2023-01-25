import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from typing import TypedDict
import json
# import uuid
import random

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "headers": "content-type",
            "Access-Control-Allow-Methods": "*"
        }
    }
)


def generate_random_id():
    return random.randint(1, 9999999)

# def generate_random_id() -> str:
#     return str(uuid.uuid4())


class FamilyType(TypedDict):
    id: int
    first_name: str
    last_name: str
    age: int
    lucky_numbers: list[int]


DB_PATH = "src/db.json"


class Writter:
    def read(self) -> list[FamilyType]:
        with open(DB_PATH, "r") as file:
            return json.loads(file.read())

    def write(self, family: list[FamilyType]) -> None:
        with open(DB_PATH, "w") as file:
            file.write(json.dumps(family))


class Family(Writter):
    def get_family(self) -> list[FamilyType]:
        return self.read()

    def add_family(self, family: FamilyType) -> None:
        family['id'] = generate_random_id()
        t = self.get_family()
        t.append(family)
        self.write(t)

    def edit_family(self, family: FamilyType) -> None:
        ts = self.get_family()
        for i, t in enumerate(ts):
            if t['id'] == family['id']:
                ts[i] = family
        self.write(ts)

    def remove_family(self, id: int) -> None:
        ts = list(filter(lambda x: x["id"] != id, self.get_family()))
        self.write(ts)


family = Family()


@app.route('/members')
def hello_world():
    return jsonify(family.get_family())


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = next((m for m in family.get_family() if m['id'] == id), None)
    if member:
        return jsonify(member)
    else:
        return jsonify({"message": "Not Found"})


@app.route('/member', methods=['POST'])
def add_new_family():
    request_body = request.get_json(force=True)
    family.add_family(request_body)
    return jsonify(family.get_family())


@app.route('/member/<int:id>', methods=['PUT'])
def put_family(id):
    request_body = request.get_json(force=True)
    family.edit_family(request_body)
    return jsonify(family.get_family())


@app.route('/member/<int:position>', methods=['DELETE'])
def delete_family(position):
    family.remove_family(id=position)
    return jsonify(family.get_family())


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
