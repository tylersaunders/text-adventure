# python3
import os

from flask import Flask, request, render_template
import logging


def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='../build',
                template_folder='../build/')

    @app.route('/')
    def index(**_):
        return render_template('index.html')

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
