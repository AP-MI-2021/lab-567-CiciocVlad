from domain.rezervare import Reservation
from server.validator import Validator
from server.service_exception import ServiceException


class Server:
    def __init__(self, reservation_repo):
        self.__reservation_repo = reservation_repo
        self.__undo_list = []

    def handle_create(self, name, reservation_class, price, check_in):
        Validator.validate_create(name, reservation_class, price, check_in)
        reservation = Reservation(name, reservation_class, float(price), check_in)
        self.__reservation_repo.create(reservation)
        self.__undo_list.append({'delete', reservation.id})

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
        self.__undo_list.append({'update': reservation})

    def handle_delete(self, reservation_id):
        if not (reservation := self.__reservation_repo.delete(reservation_id)):
            raise ServiceException('invalid reservation id')
        self.__undo_list.append({'create': reservation})

    def get_upper_class(self, name):
        reservation = self.__reservation_repo.get_by_name(name)
        if reservation is None:
            raise ServiceException('no reservation with that name found')
        if reservation.reservation_class != 'business':
            classes = ['economy', 'economy plus', 'business']
            reservation.reservation_class = classes[classes.index(reservation.reservation_class) + 1]
        return reservation

    def update_upper_class(self, name):
        self.__undo_list.append({'update_all': self.__reservation_repo.read()})
        self.__reservation_repo.update(self.get_upper_class(name))

    def get_cheaper(self, percent):
        self.__undo_list.append({'update_all': self.__reservation_repo.read()})
        for i in self.__reservation_repo.read():
            if i.check_in == 'yes':
                i.price -= (i.price * percent / 100)
                self.__reservation_repo.update(i)

    def get_highest_for_every_class(self):
        highest_price = [0, 0, 0]
        classes = ['economy', 'economy plus', 'business']
        for i in self.__reservation_repo.read():
            index = classes.index(i.reservation_class)
            highest_price[index] = i.price if i.price > highest_price[index] else highest_price[index]
        return highest_price

    def get_reservations_by_price(self):
        return sorted(self.__reservation_repo.read(), key=lambda x: x.price, reverse=True)

    def get_price_for_every_name(self):
        reservations = {x.name: 0 for x in self.__reservation_repo.read()}
        for i in self.__reservation_repo.read():
            reservations[i.name] += i.price
        return reservations

    def undo(self):
        undo_action = self.__undo_list.pop(-1)
        action = list(undo_action.keys())[0]
        value = list(undo_action.values())[0]

