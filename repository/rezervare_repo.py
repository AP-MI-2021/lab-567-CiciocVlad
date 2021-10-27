class ReservationRepo:
    def __init__(self):
        self.__id = 1
        self.__repo = {}

    def create(self, reservation):
        reservation.id = self.__id
        self.__id += 1
        self.__repo[str(reservation.id)] = reservation

    def read(self):
        return self.__repo

    def read_one(self, reservation_id):
        return self.__repo[reservation_id]

    def update(self, new_reservation):
        self.__repo[new_reservation.id] = new_reservation

    def delete(self, reservation_id):
        self.__repo.pop(reservation_id)
