from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import controllers.servidores as servidorController
import argparse
import logging
import json
import os

def load_configuration(config_file):
    filename = config_file
    if not os.path.dirname(os.path.dirname(config_file)):
        filename = os.path.dirname(__file__) + "/" + config_file

    if not os.path.isfile(filename):
        logging.error("Database config file is missing")
        # TODO raise exception

    configuration = json.load(open(filename))
    return configuration


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='"API Servidor" to provide/handle employee\'s data.')
    parser.add_argument("-c", "--config", 
                            help="Database config file path", metavar="config_file")
    args = parser.parse_args()

    server_config = {}
    if args.config:
        server_config = load_configuration(args.config)
    else: 
        server_config = load_configuration(os.path.dirname(os.path.abspath(__file__)) +"/conf.json")
    servidorController.configure_params(server_config['DatabaseHost'], server_config['DatabaseName'], server_config['DatabaseUser'], server_config['DatabasePassword'])


    with Configurator() as config:
        config.add_route('getServidores', '/api/servidores/')
        config.add_view(servidorController.get_all_employees_api , route_name='getServidores')


        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()