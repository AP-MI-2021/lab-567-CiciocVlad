from domain.rezervare import Reservation
from server.validator import Validator
from server.service_exception import ServiceException
from copy import deepcopy


class Server:
    def __init__(self, reservation_repo):
        self.__reservation_repo = reservation_repo
        self.__undo_list = []
        self.__redo_list = []

    def handle_create(self, name, reservation_class, price, check_in):
        # validates fields and creates a reservation
        # :param name: string
        # :param reservation_class: string ("economy"/"economy_plus"/"business")
        # :param price: float
        # :param check_in: string ("yes"/"no")
        # :return: void
        Validator.validate_create(name, reservation_class, price, check_in)
        reservation = Reservation(name, reservation_class, float(price), check_in)
        self.__reservation_repo.create(reservation)
        self.__undo_list.append({'delete': reservation})
        self.__redo_list.clear()

    def handle_get_all(self):
        # :return: all reservations from repository
        return self.__reservation_repo.read()

    def handle_get_one(self, reservation_id):
        # :param reservation_id: int
        # :return: reservation with the given id
        # :raises: if the id does not exist, raises KeyError
        return self.__reservation_repo.read_one(reservation_id)

    def handle_update(self, new_reservation):
        # updates reservation that has new_reservation id with new_reservation
        # :param new_reservation: Reservation
        # :return: void
        # :raises: ServiceException if the id of new_reservation does not exist
        try:
            reservation = self.__reservation_repo.read_one(new_reservation.id)
        except KeyError as e:
            raise ServiceException(e)
        new_reservation = Validator.validate_update(reservation, new_reservation)
        self.__reservation_repo.update(new_reservation)
        self.__undo_list.append({'update': reservation})
        self.__redo_list.clear()

    def handle_delete(self, reservation_id):
        # deletes the reservation with given reservation_id as a parameter
        # :param reservation_id: int
        # :return: recently deleted reservation
        # :raises: ServiceException if given id does not exist
        if not (reservation := self.__reservation_repo.delete(reservation_id)):
            raise ServiceException('invalid reservation id')
        self.__undo_list.append({'create': reservation})
        self.__redo_list.clear()
        return reservation

    def get_upper_class(self, name):
        # updates the reservation class for a reservation made on a given name
        # :param name: string
        # :return: the new reservation with updated class
        # :raises: ServiceException if name was not found
        reservations = self.__reservation_repo.get_by_name(name)
        if not reservations:
            raise ServiceException('no reservations with that name found')
        for reservation in reservations:
            if reservation.reservation_class != 'business':
                classes = ['economy', 'economy_plus', 'business']
                reservation.reservation_class = classes[classes.index(reservation.reservation_class) + 1]
        return reservations

    def update_upper_class(self, name):
        # updates the repository with the updated classes for given name
        # :param name: string
        # :return: void
        self.__undo_list.append({'update_all_names': deepcopy(self.__reservation_repo.get_by_name(name))})
        self.__redo_list.clear()
        self.__reservation_repo.update_all_names(self.get_upper_class(name))

    def get_cheaper(self, percent):
        # lower the price of all reservations that have check in by {percent}%
        # :param percent: integer
        # :return: void
        self.__undo_list.append({'update_all': deepcopy(self.__reservation_repo.read())})
        self.__redo_list.clear()
        for i in self.__reservation_repo.read():
            if i.check_in == 'yes':
                i.price -= (i.price * percent / 100)
                self.__reservation_repo.update(i)

    def get_highest_for_every_class(self):
        # :return: the highest price for every reservation class
        highest_price = [0, 0, 0]
        classes = ['economy', 'economy_plus', 'business']
        for i in self.__reservation_repo.read():
            index = classes.index(i.reservation_class)
            highest_price[index] = i.price if i.price > highest_price[index] else highest_price[index]
        return highest_price

    def get_reservations_by_price(self):
        # :return: sorted array by highest price
        return sorted(self.__reservation_repo.read(), key=lambda x: x.price, reverse=True)

    def get_price_for_every_name(self):
        # get the price of all reservations for every name
        # :return: dictionary, key being the name, value being the sum of prices of every
        # reservation made on that name
        reservations = {x.name: 0 for x in self.__reservation_repo.read()}
        for i in self.__reservation_repo.read():
            reservations[i.name] += i.price
        return reservations

    def undo(self):
        # undo the last action
        # :return: void
        undo_action = self.__undo_list.pop()
        action, *_ = undo_action.keys()
        value, *_ = undo_action.values()
        if action == 'create':
            self.__reservation_repo.create(value)
            self.__redo_list.append({'delete': value})
        if action == 'delete':
            self.__reservation_repo.delete(value.id)
            self.__redo_list.append({'create': value})
        if action == 'update':
            self.__redo_list.append({'update': self.__reservation_repo.read_one(value.id)})
            self.__reservation_repo.update(value)
        if action == 'update_all':
            self.__redo_list.append({'update_all': self.__reservation_repo.read()})
            self.__reservation_repo.update_all(value)
        if action == 'update_all_names':
            self.__redo_list.append({'update_all_names': self.__reservation_repo.get_by_name(value[0].name)})
            self.__reservation_repo.update_all_names(value)

    def redo(self):
        # redo the last undo
        # :return: void
        redo_action = self.__redo_list.pop()
        action, *_ = redo_action.keys()
        value, *_ = redo_action.values()
        if action == 'create':
            self.__reservation_repo.create(value)
            self.__undo_list.append({'delete': value})
        if action == 'delete':
            self.__reservation_repo.delete(value.id)
            self.__undo_list.append({'create': value})
        if action == 'update':
            self.__undo_list.append({'update': self.__reservation_repo.read_one(value.id)})
            self.__reservation_repo.update(value)
        if action == 'update_all':
            self.__undo_list.append({'update_all': deepcopy(self.__reservation_repo.read())})
            self.__reservation_repo.update_all(value)
        if action == 'update_all_names':
            self.__undo_list.append({'update_all_names': deepcopy(self.__reservation_repo.get_by_name(value[0].name))})
            self.__reservation_repo.update_all_names(value)
