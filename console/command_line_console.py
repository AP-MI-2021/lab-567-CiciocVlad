from domain.rezervare import Reservation
from server.service_exception import ServiceException


class CLIConsole:
    def __init__(self, reservation_service):
        self.__reservation_service = reservation_service

    def handle_menu(self):
        print('type help for command info')
        while (option := input()) != 'quit':
            if option == 'help':
                print('to create a new reservation type: add `reservation_name` `class` `price` `check_in`')
                print('to delete a reservation type: delete `reservation_id`')
                print('to update a reservation type: update `id` `reservation_name` `class` `price` `check_in`')
                print('if you want to leave some fields as they were, leave an empty space in their place as they '
                      'are in the update command')
                print('to get all reservations type: get')
                print('to get one reservation type: get `id`')
            else:
                tokens = option.split(' ')
                if tokens[0] == 'add':
                    try:
                        if len(tokens) != 5:
                            print('invalid options')
                        else:
                            self.__reservation_service.handle_create(tokens[1], tokens[2], tokens[3], tokens[4])
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
                elif tokens[0] == 'delete':
                    if len(tokens) != 2:
                        print('invalid option')
                    else:
                        try:
                            self.__reservation_service.handle_delete(tokens[1])
                        except ServiceException as e:
                            print(e)
                elif tokens[0] == 'update':
                    if len(tokens) != 6:
                        print('invalid command')
                    else:
                        reservation = Reservation(tokens[2], tokens[3], tokens[4], tokens[5])
                        reservation.id = tokens[1]
                        try:
                            self.__reservation_service.handle_update(reservation)
                        except ServiceException as e:
                            print(e)
                else:
                    print('invalid option')
