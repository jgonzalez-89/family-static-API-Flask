from random import randint

#La clase Family se utiliza para crear una familia con un apellido específico y miembros predefinidos. El método init se ejecuta automáticamente al crear una nueva instancia de la clase y establece el apellido de la familia y los miembros predefinidos.
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [{"id": 1,
                          "first_name": "John",
                          "last_name": last_name,
                          "age": 33,
                          "lucky_numbers": [7, 13, 22]},
                         {"id": 2,
                          "first_name": "Jane",
                          "last_name": last_name,
                          "age": 35,
                          "lucky_numbers": [10, 14, 3]},
                         {"id": 3,
                          "first_name": "Jimmy",
                          "last_name": last_name,
                          "age": 5,
                          "lucky_numbers": [1]}]

    #El método _generateId genera un número aleatorio entre 1 y 99999999, que se utiliza como identificador para cada miembro de la familia.
    def _generateId(self):
        return randint(1, 99999999)

    #El método add_member agrega un nuevo miembro a la familia y establece su apellido igual al apellido de la familia.
    def add_member(self, member):
        member["last_name"] = self.last_name
        self._members.append(member)
        return self._members

    #El método delete_member elimina un miembro de la familia con el identificador especificado.
    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True

        return False

    #El método get_member devuelve el miembro de la familia con el identificador especificado.
    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member

    #El método get_all_members devuelve una lista con todos los miembros de la familia.
    def get_all_members(self):
        return self._members
