# -*- coding: UTF-8 -*-
"""Defines the CLI for displaying information about Avamar servers"""
import click

from vlab_cli.lib.api import consume_task
from vlab_cli.lib.ascii_output import vm_table_view, columned_table
from vlab_cli.lib.versions import Version


@click.command()
@click.option('-i', '--images', is_flag=True,
              help='Display the available versions of Avamar server to deploy')
@click.pass_context
def avamar(ctx, images):
    """Display information about Avamar servers in your lab"""
    if images:
        info = consume_task(ctx.obj.vlab_api,
                            endpoint='/api/2/inf/avamar/server/image',
                            base_endpoint=False,
                            message='Collecting available versions of Avamar for deployment',
                            method='GET').json()['content']
        rows = []
        for img in info['image']:
            rows.append(img)
        output = get_formatted_table(sorted(rows))
        click.echo('\n{}\n'.format(output))
    else:
        info = consume_task(ctx.obj.vlab_api,
                            endpoint='/api/2/inf/avamar/server',
                            message='Collecting information about your Avamar instances',
                            method='GET').json()
        output = vm_table_view(ctx.obj.vlab_api, info['content'])
        if not output:
            output = 'You do not own any Avamar servers instances'
        click.echo(output)


def get_formatted_table(images):
    """A human handy table of the different variants of Avamar server, and versions
    that can be deployed.

    :Returns: String

    :param images: The available version/images of Avamar server, ordered by version number
    :type images: List
    """
    header = ['Avamar']
    table = columned_table(header, [images])
    return table
