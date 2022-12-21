"""Command line interface for Diligent."""

import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Diligent command line interface."""


@cli.command()
def start():
    """Start the Diligent server."""
    print("Starting Diligent server...")


@cli.command()
def stop():
    """Stop the Diligent server."""
    print("Stopping Diligent server...")
