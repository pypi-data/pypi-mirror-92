import click

from .init import init_project


@click.group()
def project_group():
    pass


project_group.add_command(init_project, 'init')
