from server.validator import Validator
from server.service_exception import ServiceException


class Server:
    def __init__(self, reservation_repo):
        self.__reservation_repo = reservation_repo

    def handle_create(self, reservation):
        Validator.validate_create(reservation)
        self.__reservation_repo.create(reservation)

    def handle_get_all(self):
        return self.__reservation_repo.read()

    def handle_get_one(self, reservation_id):
        return self.__reservation_repo.read_one(reservation_id)

    def handle_update(self, new_reservation):
        try:
            reservation = self.__reservation_repo.read_one(new_reservation.id)
        except KeyError as e:
            raise ServiceException(e)
        new_reservation = Validator.validate_update(reservation, new_reservation)
        self.__reservation_repo.update(new_reservation)

    def handle_delete(self, reservation_id):
        self.__reservation_repo.delete(reservation_id)
