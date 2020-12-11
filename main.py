from server import main as main_server

app = main_server.create_app()

if __name__ == '__main__':
    main_server.socket.run(app)
