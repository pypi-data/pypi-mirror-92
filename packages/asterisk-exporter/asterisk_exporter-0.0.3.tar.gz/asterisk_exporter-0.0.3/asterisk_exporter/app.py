import click
import sentry_sdk
from asterisk_exporter import __version__
from sentry_sdk.integrations.logging import LoggingIntegration
import asterisk_exporter.exporter as exporter
import logging
import os

sentry_dsn =  os.environ.get('SENTRY_DSN')
if sentry_dsn:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.CRITICAL
    )

    sentry_sdk.init(
        sentry_dsn,
        traces_sample_rate=1.0,
        release="asterisk_exporter@{}".format(__version__),
        integrations=[sentry_logging]
    )

@click.group(help='')
def cli():
    pass

@click.command()
@click.option('-h', '--host', required= True, type=str, help= "address on which to bind")
@click.option('-p', '--port', required= True, type=int, help= "port on which to bind")
@click.option('-u', '--user', required= True, type=str, help= "asterisk manager user")
@click.option('-w', '--password', required= True, type=str, help= "asterisk manager password")
def start(host, port, user, password):
    exporter.start_server(host, port, user, password)

cli.add_command(start)

if __name__ == '__main__':
    cli()
