class ReservationRepo:
    def __init__(self):
        self.__id = 1
        self.__repo = []

    def create(self, reservation):
        # generates an id, and adds a reservation to the repo
        # with the generated id to the repo
        # :param reservation: object of type Reservation
        # :return: void
        if reservation.id is None:
            reservation.id = self.__id
            self.__id += 1
        self.__repo.append(reservation)

    def read(self):
        # :return: entire list of reservations
        return self.__repo

    def read_one(self, reservation_id):
        # :param reservation_id: int
        # :return: the reservation with the given reservation id as a parameter
        for i in self.__repo:
            if i.id == int(reservation_id):
                return i
        raise KeyError('id not found')

    def get_by_name(self, name):
        # :param name: string
        # :return: the reservation on the given name as a parameter
        return list(filter(lambda x: x.name == name, self.__repo))

    def update(self, new_reservation):
        # updates the reservation that has the same id as the reservation
        # given as a parameter with the new reservation fields instead
        # :param new_reservation: Reservation
        # :return: void
        for index, i in enumerate(self.__repo):
            if i.id == new_reservation.id:
                self.__repo[index] = new_reservation

    def update_all(self, reservations):
        self.__repo = reservations

    def update_all_names(self, reservations):
        self.__repo = list(filter(lambda x: x.name != reservations[0].name, self.__repo)) + reservations

    def delete(self, reservation_id):
        # deletes the reservation with the given id
        # :param reservation_id: int
        # :return: the deleted reservation or None if the id does not exist
        for index, i in enumerate(self.__repo):
            if i.id == int(reservation_id):
                return self.__repo.pop(index)
        return None
