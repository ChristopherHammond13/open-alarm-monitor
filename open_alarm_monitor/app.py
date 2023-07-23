"""Open Alarm Monitor: Command Line Interface (CLI)."""
import os

import click

from open_alarm_monitor.accounts import Account
from open_alarm_monitor.handlers import HANDLERS
from open_alarm_monitor.server import (
    ACCOUNTS,
    AlarmServer,
)


try:
    # This is native on Python 3.11
    import tomllib
except ImportError:
    import tomli as tomllib


@click.option(
    '-c',
    '--config-file',
    type=click.STRING,
    default='config.toml',
    help='Path to the configuration file (default: config.toml)',
)
@click.command(
    name='listen',
    help='Run the alarm monitoring service',
)
def listen(config_file: str):
    """Open Alarm Monitor CLI."""
    click.echo(click.style("Open Alarm Monitor", bold=True))
    if not os.path.exists(config_file):
        click.echo(click.style(
            "Configuration file does not exist. Please specify one with -c.",
            fg='red',
            bold=True,
        ))
        return

    with open(config_file, 'rb') as f:
        config = tomllib.load(f)

    config = config['open_alarm_monitor']

    account_keys = config['accounts']
    for account_key in account_keys:
        account_data = config['accounts'][account_key]
        account_number = int(account_data['account_number'])
        account = Account(
            name=account_data['name'],
            address=account_data['address'],
            protocol=account_data['protocol'],
            account_number=account_number,
        )

        for handler_name in account_data["message_handlers"]:
            handler_config = config['message_handlers'][handler_name]
            account.handlers.append(HANDLERS[handler_config['handler_type']](handler_config))

        ACCOUNTS[account_number] = account

        listen_address = config['listen']['address']
        listen_port = config['listen']['port']

        print("Got accounts: " + str(ACCOUNTS.keys()))

        server = AlarmServer(listen_address, int(listen_port))
        server.listen()


@click.group()
def cli():
    pass


cli.add_command(listen)
