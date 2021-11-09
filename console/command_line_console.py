from domain.rezervare import Reservation
from server.service_exception import ServiceException


class CLIConsole:
    def __init__(self, reservation_service):
        self.__reservation_service = reservation_service

    def handle_menu(self):
        print('type help for command info')
        running = True
        while running:
            options = input()
            for option in options.split(';'):
                if option == 'help':
                    print('to create a new reservation type: add `reservation_name` `class` `price` `check_in`')
                    print('to delete a reservation type: delete `reservation_id`')
                    print('to update a reservation type: update `id` `reservation_name` `class` `price` `check_in`')
                    print('if you want to leave some fields as they were, leave an empty space in their place as they '
                          'are in the update command')
                    print('to get all reservations type: get')
                    print('to get one reservation type: get `id`')
                    print('to update all reservation for a given name with the upper class type: to_upper_class `name`')
                    print('to lower the price for all check in reservations type: get_lower `percent`')
                    print('to get the highest price for every class type: highest')
                    print('to get reservations sorted by price type: get_by_price')
                    print('to get price of reservations for each name type: get_by_name')
                    print('to undo type: undo')
                    print('to redo type: redo')
                    print('to exit type: quit')
                else:
                    tokens = option.split(' ')
                    if tokens[0] == 'add':
                        try:
                            if len(tokens) != 5:
                                print('invalid options')
                            else:
                                self.__reservation_service.handle_create(tokens[1], tokens[2], tokens[3], tokens[4])
                                print('created!')
                        except ServiceException as e:
                            print(e)
                    elif tokens[0] == 'get':
                        if len(tokens) == 1:
                            for i in self.__reservation_service.handle_get_all():
                                print(i)
                        else:
                            try:
                                print(self.__reservation_service.handle_get_one(tokens[1]))
                            except KeyError as e:
                                print(e)
                            except ValueError:
                                print('invalid argument')
                    elif tokens[0] == 'delete':
                        if len(tokens) != 2:
                            print('invalid option')
                        else:
                            try:
                                self.__reservation_service.handle_delete(tokens[1])
                                print('deleted!')
                            except ServiceException as e:
                                print(e)
                    elif tokens[0] == 'update':
                        if len(tokens) != 6:
                            print('invalid command')
                        else:
                            reservation = Reservation(tokens[2], tokens[3], tokens[4], tokens[5])
                            try:
                                reservation.id = int(tokens[1])
                                self.__reservation_service.handle_update(reservation)
                                print('updated!')
                            except ServiceException as e:
                                print(e)
                            except ValueError:
                                print('id must be int')
                    elif tokens[0] == 'to_upper_class':
                        if len(tokens) != 2:
                            print('invalid command')
                        else:
                            try:
                                self.__reservation_service.update_upper_class(tokens[1])
                                print('updated!')
                            except ServiceException as e:
                                print(e)
                    elif tokens[0] == 'get_lower':
                        if len(tokens) != 2:
                            print('invalid command')
                        else:
                            try:
                                self.__reservation_service.get_cheaper(float(tokens[1]))
                                print('updated prices')
                            except ValueError:
                                print('percentage must be a float value')
                    elif tokens[0] == 'highest':
                        if len(tokens) != 1:
                            print('this command does not take any params')
                        else:
                            [economy, economy_plus, business] = self.__reservation_service.get_highest_for_every_class()
                            if economy > 0:
                                print(f'highest price for economy class: {economy}')
                            if economy_plus > 0:
                                print(f'highest price for economy plus class: {economy_plus}')
                            if business > 0:
                                print(f'highest price for business class: {business}')
                    elif tokens[0] == 'get_by_price':
                        if len(tokens) != 1:
                            print('this command does not take any params')
                        else:
                            for i in self.__reservation_service.get_reservations_by_price():
                                print(i)
                    elif tokens[0] == 'get_by_name':
                        if len(tokens) != 1:
                            print('this command does not take any params')
                        else:
                            prices = self.__reservation_service.get_price_for_every_name()
                            for i in prices.keys():
                                print(f'name: {i}\nprice: {prices[i]}\n')
                    elif tokens[0] == 'undo':
                        try:
                            self.__reservation_service.undo()
                            print('reversed last command!')
                        except IndexError:
                            print('no undo left')
                    elif tokens[0] == 'redo':
                        try:
                            self.__reservation_service.redo()
                            print('reversed last undo!')
                        except IndexError:
                            print('no redo left')
                    elif tokens[0] == 'quit':
                        running = False
                    else:
                        print('invalid option')
