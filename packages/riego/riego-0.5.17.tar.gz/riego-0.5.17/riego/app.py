import asyncio
import configargparse
import pkg_resources
import os
import pathlib
# import logging
# import sys
import socket

import riego.database
import riego.valves
import riego.parameter
import riego.mqtt_gmqtt as riego_mqtt
import riego.logger
import riego.timer
import riego.boxes

from riego.web.routes import setup_routes
from riego.web.error_pages import setup_error_pages
from riego.web.websockets import setup_websockets

from aiohttp import web
import jinja2
import aiohttp_jinja2
import aiohttp_debugtoolbar

from riego.__init__ import __version__


async def on_startup(app):
    if app['options'].enable_asyncio_debug:
        asyncio.get_event_loop().set_debug(True)
    app['log'].info("on_startup")
# TODO bring next two lines to correspondending classes
    app['background_mqtt'] = asyncio.create_task(app['mqtt'].start_async())
    app['background_timer'] = asyncio.create_task(app['timer'].start_async())


async def on_shutdown(app):
    app['log'].info("on_shutdown")


async def on_cleanup(app):
    app['log'].info("on_cleanup")

    app['background_timer'].cancel()
    await app['background_timer']

    app['background_mqtt'].cancel()
    await app['background_mqtt']


def main():
    p = configargparse.ArgParser(
        default_config_files=['/etc/riego/conf.d/*.conf', '~/.riego.conf',
                              'riego.conf'])
    p.add('-c', '--config', is_config_file=True, env_var='RIEGO_CONF',
          required=False, help='config file path')
    p.add('-d', '--database', help='Path and name for DB file',
          default='db/riego.db')
    p.add('-e', '--event_log', help='Full path and name for event logfile',
          default='log/event.log')
    p.add('--event_log_max_bytes', help='Maximum Evet Log Size in bytes',
          default=1024*300, type=int)
    p.add('--event_log_backup_count', help='How many files to rotate',
          default=3, type=int)
    p.add('-m', '--mqtt_host', help='IP adress of mqtt host',
          default='127.0.0.1')
    p.add('-p', '--mqtt_port', help='Port of mqtt service',
          default=1883, type=int)
    p.add('--mqtt_client_id', help='Client ID for MQTT-Connection',
          default=f'riego_ctrl_{socket.gethostname()}')
    p.add('--mqtt_subscription_topic', help='MQTT Topic that we are listening',
          default='riego/#')
    p.add('--database_migrations_dir',
          help='path to database migrations directory',
          default=pkg_resources.resource_filename('riego', 'migrations'))
    p.add('--base_dir', help='Change only if you know what you are doing',
          default=pathlib.Path(__file__).parent)
    p.add('--http_server_bind_address',
          help='http-server bind address', default='0.0.0.0')
    p.add('--http_server_bind_port', help='http-server bind port',
          default=8080, type=int)
    p.add('--http_server_static_dir',
          help='Serve static html files from this directory',
          default=pkg_resources.resource_filename('riego.web', 'static'))
    p.add('--http_server_template_dir',
          help='Serve template files from this directory',
          default=pkg_resources.resource_filename('riego.web', 'templates'))
    p.add('--websocket_path', help='url path for websocket',
          default="/ws")
    p.add('--time_format', help='Store and display time',
          default="%Y-%m-%d %H:%M:%S")
    p.add('--mqtt_cmnd_prefix', help='',
          default="cmnd")
    p.add('--mqtt_result_subscription', help='',
          default="stat/+/RESULT")
    p.add('--mqtt_status_subscription', help='yet not used',
          default="stat/+/STATUS")
    p.add('--mqtt_tele_subscription', help='yet not used',
          default="tele/#")
    p.add('--mqtt_tele_filter_LWT', help='yet not used',
          default="tele/+/LWT")
    p.add('--mqtt_tele_filter_SENSOR',
          help='yet not used', default="tele/+/SENSOR")
    p.add('--mqtt_tele_filter_state', help='yet not used',
          default="tele/+/state")
    p.add('--mqtt_keyword_ON', help='',
          default="ON")
    p.add('--mqtt_keyword_OFF', help='',
          default="OFF")

    p.add('--enable_aiohttp_debug_toolbar', action='store_true')
    p.add('--enable_asyncio_debug', action='store_true')
    p.add('--enable_timer_dev_mode', action='store_true')

    p.add('-v', '--verbose', help='verbose', action='store_true')
    p.add('--version', help='Print version and exit', action='store_true')
    p.add('--defaults', help='Print options with default values and exit',
          action='store_true')

    options = p.parse_args()

    try:
        with open('riego.conf', 'xt') as f:
            for item in vars(options):
                f.write(f'# {item}={getattr(options, item)}\n')
    except IOError:
        pass

    if options.defaults:
        for item in vars(options):
            print(f'# {item}={getattr(options, item)}')
        exit(0)

    if options.version:
        print('Version: ', __version__)
        exit(0)

    if options.verbose:
        print(p.format_values())

#    if sys.version_info >= (3, 8):
#        asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy  # noqa: E501

    if os.name == "posix":
        import uvloop  # pylint: disable=import-error
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application()

    app['version'] = __version__
    app['options'] = options
    app['log'] = riego.logger.create_log(options)
    app['event_log'] = riego.logger.create_event_log(options)
    app['db'] = riego.database.Database(app)
    app['mqtt'] = riego_mqtt.Mqtt(app)
# boxes evtl. vor den Valves starten => MQTT -LWT nachrichten
    app['valves'] = riego.valves.Valves(app)
    app['parameter'] = riego.parameter.Parameter(app)
    app['timer'] = riego.timer.Timer(app)
    app['boxes'] = riego.boxes.Boxes(app)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    app.on_cleanup.append(on_cleanup)

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(
                             options.http_server_template_dir))

    setup_routes(app)
    setup_error_pages(app)
    setup_websockets(app)

    if options.enable_aiohttp_debug_toolbar:
        aiohttp_debugtoolbar.setup(app, check_host=False)

    app['log'].info("Start")
    app['event_log'].info('Start')

    web.run_app(app,
                host=options.http_server_bind_address,
                port=options.http_server_bind_port)
