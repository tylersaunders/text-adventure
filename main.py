import logging
from server import main as main_server

logging.basicConfig(level=logging.DEBUG)
app = main_server.create_app()

if __name__ == '__main__':
    logging.info("text-adventure app created successfully! \o/")
    main_server.socket.run(app, host='0.0.0.0', port=8080)
