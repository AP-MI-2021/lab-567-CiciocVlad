from repository.rezervare_repo import ReservationRepo
from server.server import Server
from console.console import Console


def main():
    reservation_repo = ReservationRepo()
    server = Server(reservation_repo)
    console = Console(server)
    console.handle_menu()


if __name__ == '__main__':
    main()
