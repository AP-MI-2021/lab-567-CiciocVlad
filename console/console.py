from domain.rezervare import Reservation
from server.service_exception import ServiceException


class Console:
    def __init__(self, reservation_service):
        self.__reservation_service = reservation_service

    @staticmethod
    def menu():
        print('1. create reservation')
        print('2. get all')
        print('3. get one')
        print('4. update reservation')
        print('5. delete reservation')
        print('6. exit')
        return input('your option: ')

    def handle_menu(self):
        while (option := self.menu()) != '6':
            if option == '1':
                name = input('name: ')
                reservation_class = input('class: ')
                price = input('price: ')
                check_in = input('check in: ')
                try:
                    self.__reservation_service.handle_create(Reservation(name, reservation_class, price, check_in))
                except ServiceException as e:
                    print(e)
            elif option == '2':
                for i in self.__reservation_service.handle_get_all():
                    print(i)
            elif option == '3':
                try:
                    print(self.__reservation_service.handle_get_one(input('id: ')))
                except KeyError:
                    print('id not found')
            elif option == '4':
                reservation_id = input('id: ')
                name = input('name: ')
                reservation_class = input('reservation_class: ')
                price = input('price: ')
                check_in = input('check in: ')
                reservation = Reservation(name, reservation_class, price, check_in)
                reservation.id = reservation_id
                try:
                    self.__reservation_service.handle_update(reservation)
                except ServiceException as e:
                    print(e)
            elif option == '5':
                reservation_id = input('id: ')
                self.__reservation_service.handle_delete(reservation_id)
            else:
                print('invalid option')
