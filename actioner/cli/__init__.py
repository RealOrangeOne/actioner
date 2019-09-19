import click

from actioner.clients import get_todoist_client


def list_todoist_projects():
    todoist = get_todoist_client()
    todoist.projects.sync()

    for project in todoist.state["projects"]:
        click.echo("'{}' has id {}".format(project["name"], project["id"]))


CLI_ENTRYPOINTS = [list_todoist_projects]
