class Reservation:
    def __init__(self, name, reservation_class, price, check_in):
        self.__id = 0
        self.__name = name
        self.__reservation_class = reservation_class
        self.__price = price
        self.__check_in = check_in

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def reservation_class(self):
        return self.__reservation_class

    @property
    def price(self):
        return self.__price

    @property
    def check_in(self):
        return self.__check_in

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @reservation_class.setter
    def reservation_class(self, new_reservation_class):
        self.__reservation_class = new_reservation_class

    @price.setter
    def price(self, new_price):
        self.__price = new_price

    @check_in.setter
    def check_in(self, new_check_in):
        self.__check_in = new_check_in

    def __str__(self):
        return f'\nid: {self.id}\nname: {self.name}\nclass: {self.reservation_class}\n' \
               f'price: {self.price}\ncheck in: {self.check_in}\n'
