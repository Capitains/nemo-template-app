from nemo.app import app, configurable
import click


@click.group("Commandes for Nemo")
def nemo_template_cli():
    """ Generic CLI for Nemo applications
    """


@nemo_template_cli.command("cache-clear")
def parse():
    configurable.resolver.cache.clear()


@nemo_template_cli.command("cache-parse")
def parse():
    configurable.resolver.cache.clear()
    configurable.resolver.parse()


@nemo_template_cli.command("dev-run")
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def dev_run(port=5000):
    """ This command should only be run for development """
    configurable.resolver.cache.clear()
    app.debug = True
    app.run(port=port)


if __name__ == "__main__":
    nemo_template_cli()