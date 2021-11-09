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
        print('6. get every reservation upper class for name')
        print('7. get all check in cheaper')
        print('8. get highest price for every class')
        print('9. get reservations by price')
        print('10. show price for every name')
        print('11. undo')
        print('12. redo')
        print('x. exit')
        return input('your option: ')

    def handle_menu(self):
        while (option := self.menu()) != 'x':
            if option == '1':
                name = input('name: ')
                reservation_class = input('class: ')
                price = input('price: ')
                check_in = input('check in: ')
                try:
                    self.__reservation_service.handle_create(name, reservation_class, price, check_in)
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
                reservation_class = input('class: ')
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
                try:
                    self.__reservation_service.handle_delete(reservation_id)
                except ServiceException as e:
                    print(e)
            elif option == '6':
                name = input('name: ')
                try:
                    self.__reservation_service.update_upper_class(name)
                except ServiceException as e:
                    print(e)
            elif option == '7':
                try:
                    percent = int(input('percent: '))
                    self.__reservation_service.get_cheaper(percent)
                except ValueError:
                    print('percent must be an int value')
            elif option == '8':
                [economy, economy_plus, business] = self.__reservation_service.get_highest_for_every_class()
                if economy > 0:
                    print(f'highest price for economy class: {economy}')
                if economy_plus > 0:
                    print(f'highest price for economy plus class: {economy_plus}')
                if business > 0:
                    print(f'highest price for business class: {business}')
            elif option == '9':
                for i in self.__reservation_service.get_reservations_by_price():
                    print(i)
            elif option == '10':
                prices = self.__reservation_service.get_price_for_every_name()
                for i in prices.keys():
                    print(f'name: {i}\nprice: {prices[i]}\n')
            elif option == '11':
                try:
                    self.__reservation_service.undo()
                except IndexError:
                    print('no undo left')
            elif option == '12':
                try:
                    self.__reservation_service.redo()
                except IndexError:
                    print('no redo left')
            else:
                print('invalid option')
