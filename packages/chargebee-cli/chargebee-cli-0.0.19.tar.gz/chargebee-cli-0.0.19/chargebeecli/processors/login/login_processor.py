import click

from chargebeecli.config.Configuration import Configuration


def process(profile):
    configuration = Configuration.Instance()
    if profile in configuration.fetch_available_sections():
        configuration.update_section("active_profile", {'primary': profile})
        click.echo(f"{profile} active profile set")
    else:
        click.echo(f"{profile}: profile does not exist", err=True)
