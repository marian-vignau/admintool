"""

"""
__author__ = "Maria Andrea Vignau"

import click
from mod.drives import Drives
from mod import scanner
from mod import api

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command()
def drives():
    """Print symbolic drives information.
    Don't use elevated privileges to see network attached drives."""
    click.echo(Drives)


@cli.command()
@click.argument('operation', type=click.Choice(["list", "purposes", "remove", "scan"]),
                default="list"
                )
@click.argument('name', type=str, default="")
def storage(operation, name):
    """Manage storage. List your own storage & check mounted, remove them,  or list possible purposes."""
    if operation == "purposes":
        click.echo('; '.join(scanner.storage_types))
    if operation == "list":
        for idx, storage in enumerate(api.storagelist()):
            currentpath = Drives.find_path(storage.drivename, storage.parentdir)
            if not currentpath:
                currentpath = "unavailable"
            line = """<{1.name}> {1.purpose}|{2} => "{1.drivename}{1.parentdir}" ?="{1.description}" """
            line = line.format(idx + 1, storage, currentpath)
            click.echo(line)
        click.echo("Founded %d storage" % (idx + 1))

    if operation == "remove":
        if api.storagedel(name):
            click.echo('remove storage %s' % name)

    if operation == "scan":
        obj = api.storagescan(name)
        if obj:
            click.echo('scan storage %s' % str(obj))


@cli.command()
@click.pass_context
@click.option('-n', '--name', type=str,
              prompt='Name',
              help='Unique identifier name of added storage')
@click.option('-d', '--drive', type=click.Choice(Drives.current_names()),
              prompt='Drivename',
              help='Use a symbolic drive name o real one')
@click.option('-p', '--parentdir', type=str, default="\\",
              prompt='Path to the folder',
              help='Subfolder path. Defaults to root folder')
@click.option('-t', '--type', "_type", type=click.Choice(scanner.storage_types),
              prompt='Purpose of storage to add',
              help='Purpose of storage')
@click.option('-c', '--description', type=str,
              prompt='Title or description',
              help='Title or description')
def storage_add(ctx, name, drive, parentdir, _type, description):
    """Add an storage. """
    if drive.endswith(":"):
        drivename = Drives.find_drivename(drive[0])
    else:
        drivename = drive
    api.storageadd(name, drivename, parentdir, _type, description)


@cli.command()
@click.pass_context
@click.argument('operation', type=click.Choice(["list", "purposes", "remove", "show"]),
                default="list"
                )
@click.argument('name', type=str, default="")
def reports(ctx, operation, name):
    if operation == "list":
        idx = 0
        for idx, report in enumerate(api.reportlist()):
            line = """<{1.reportname}> """
            line = line.format(idx + 1, report)
            click.echo(line)
        click.echo("Founded %d reports" % (idx + 1))

    elif operation == "show":
        for line in api.reportinfo(name.upper()):
            click.echo(line)


@cli.command()
def wipescanned():
    """ Delete all scanned info."""
    api.wipescannedinfo()
    click.echo("deleted all scanned info")


@cli.command()
@click.pass_context
def info(ctx):
    """Show information"""
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
