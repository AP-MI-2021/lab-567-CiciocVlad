from repository.rezervare_repo import ReservationRepo
from server.server import Server
from console.command_line_console import CLIConsole


def main():
    reservation_repo = ReservationRepo()
    server = Server(reservation_repo)
    console = CLIConsole(server)
    console.handle_menu()


if __name__ == '__main__':
    main()
