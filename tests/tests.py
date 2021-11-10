from domain.rezervare import Reservation
from repository.rezervare_repo import ReservationRepo
from server.server import Server
from server.service_exception import ServiceException


def test_handle_create(server):
    server.handle_create('Jane', 'business', '100', 'yes')
    assert len(server.handle_get_all()) == 1
    try:
        server.handle_create('John', 'class', '20', 'no')
        assert False
    except ServiceException:
        assert True


def test_handle_get_all(server):
    reservation = Reservation('Jane', 'business', float('100'), 'yes')
    reservation.id = 1
    assert server.handle_get_all() == [reservation]


def test_handle_get_one(server):
    reservation = Reservation('Jane', 'business', float('100'), 'yes')
    reservation.id = 1
    assert server.handle_get_one(1) == reservation
    try:
        server.handle_get_one(2)
        assert False
    except KeyError:
        assert True


def test_handle_delete(server):
    reservation = server.handle_delete(1)
    res = Reservation('John', 'economy_plus', float('90'), 'yes')
    res.id = 1
    assert reservation == res
    assert len(server.handle_get_all()) == 0
    try:
        server.handle_delete(1)
        assert False
    except ServiceException:
        assert True


def test_handle_update(server):
    new_reservation = Reservation('John', 'economy', float('100'), 'yes')
    new_reservation.id = 1
    server.handle_update(new_reservation)
    assert server.handle_get_all() == [new_reservation]


def test_update_upper_class(server):
    server.update_upper_class('John')
    reservation_result = Reservation('John', 'economy_plus', float('100'), 'yes')
    reservation_result.id = 1
    assert server.handle_get_all() == [reservation_result]


def test_get_cheaper(server):
    server.get_cheaper(10)
    reservation_result = Reservation('John', 'economy_plus', float('90'), 'yes')
    reservation_result.id = 1
    assert server.handle_get_all() == [reservation_result]


def test_get_higher_for_every_class(server):
    assert server.get_highest_for_every_class() == [0, 90, 0]


def test_get_reservations_by_price(server):
    assert server.get_reservations_by_price() == server.handle_get_all()


def test_get_price_for_every_name(server):
    assert server.get_price_for_every_name() == {'John': 90}


def test_undo(server):
    server.undo()
    reservation_result = Reservation('John', 'economy_plus', float('100'), 'yes')
    reservation_result.id = 1
    assert server.handle_get_all() == [reservation_result]


def test_redo(server):
    server.redo()
    reservation_result = Reservation('John', 'economy_plus', float('90'), 'yes')
    reservation_result.id = 1
    assert server.handle_get_all() == [reservation_result]


def test_general(server):
    assert server.handle_get_all() == []
    reservation1 = Reservation('Jane', 'economy', float('50'), 'yes')
    reservation1.id = 2
    server.handle_create('Jane', 'economy', '50', 'yes')
    assert len(server.handle_get_all()) == 1
    reservation2 = Reservation('John', 'business', float('100'), 'yes')
    reservation2.id = 3
    server.handle_create('John', 'business', '100', 'yes')
    assert len(server.handle_get_all()) == 2
    reservation3 = Reservation('Jane', 'economy_plus', float('90'), 'no')
    reservation3.id = 4
    server.handle_create('Jane', 'economy_plus', '90', 'no')
    assert len(server.handle_get_all()) == 3
    server.undo()
    assert server.handle_get_all() == [reservation1, reservation2]
    server.undo()
    server.undo()
    try:
        server.undo()
        assert False
    except IndexError:
        assert True
    assert server.handle_get_all() == []
    server.handle_create('Jane', 'economy', '50', 'no')
    server.handle_create('John', 'business', '100', 'yes')
    server.handle_create('Jane', 'economy_plus', '90', 'yes')
    try:
        server.redo()
        assert False
    except IndexError:
        assert True
    assert len(server.handle_get_all()) == 3
    server.undo()
    server.undo()
    assert len(server.handle_get_all()) == 1
    server.redo()
    assert len(server.handle_get_all()) == 2
    server.redo()
    assert len(server.handle_get_all()) == 3
    server.undo()
    server.undo()
    assert len(server.handle_get_all()) == 1
    server.redo()
    server.redo()
    assert len(server.handle_get_all()) == 3
    server.undo()
    server.undo()
    assert len(server.handle_get_all()) == 1
    server.handle_create('Marcel', 'business', '150', 'yes')
    try:
        server.redo()
        assert False
    except IndexError:
        assert True
    server.undo()
    server.undo()
    assert server.handle_get_all() == []
    server.redo()
    server.redo()
    assert len(server.handle_get_all()) == 2
    try:
        server.redo()
        assert False
    except IndexError:
        assert True


def run_tests():
    repo = ReservationRepo()
    server = Server(repo)
    test_handle_create(server)
    test_handle_get_all(server)
    test_handle_get_one(server)
    test_handle_update(server)
    test_update_upper_class(server)
    test_get_cheaper(server)
    test_get_higher_for_every_class(server)
    test_get_reservations_by_price(server)
    test_get_price_for_every_name(server)
    test_undo(server)
    test_redo(server)
    test_handle_delete(server)
    server = Server(repo)
    test_general(server)
