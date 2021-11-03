class ReservationRepo:
    def __init__(self):
        self.__id = 1
        self.__repo = []

    def create(self, reservation):
        reservation.id = self.__id
        self.__id += 1
        self.__repo.append(reservation)

    def read(self):
        return self.__repo

    def read_one(self, reservation_id):
        for i in self.__repo:
            if i.id == int(reservation_id):
                return i
        raise KeyError('id not found')

    def get_by_name(self, name):
        for i in self.__repo:
            if i.name == name:
                return i
        return None

    def update(self, new_reservation):
        for index, i in enumerate(self.__repo):
            if i.id == int(new_reservation.id):
                self.__repo[index] = new_reservation

    def delete(self, reservation_id):
        for index, i in enumerate(self.__repo):
            if i.id == int(reservation_id):
                return self.__repo.pop(index)
        return None
