from server.service_exception import ServiceException


class Validator:
    @staticmethod
    def validate_create(_name, reservation_class, price, check_in):
        try:
            float(price)
        except ValueError:
            raise ServiceException('price must be a float')
        if reservation_class not in ['economy', 'economy plus', 'business']:
            raise ServiceException('invalid reservation class, could not create')
        if check_in not in ['yes', 'no']:
            raise ServiceException('invalid check in, could not create')

    @staticmethod
    def validate_update(reservation, new_reservation):
        if new_reservation.name == '':
            new_reservation.name = reservation.name
        if new_reservation.reservation_class == '':
            new_reservation.reservation_class = reservation.reservation_class
        if new_reservation.price == '':
            new_reservation.price = float(reservation.price)
        if new_reservation.check_in == '':
            new_reservation.check_in = reservation.check_in
        if new_reservation.reservation_class not in ['economy', 'economy plus', 'business']:
            raise ServiceException('invalid reservation class, could not update')
        if new_reservation.check_in not in ['yes', 'no']:
            raise ServiceException('invalid check in, could not update')
        return new_reservation
