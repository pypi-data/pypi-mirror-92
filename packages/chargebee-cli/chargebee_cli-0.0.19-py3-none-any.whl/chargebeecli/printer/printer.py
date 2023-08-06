import click
from tabulate import tabulate


def custom_print(message, err=False):
    if err is not True:
        click.secho(message, err=True, nl=True)
    else:
        click.secho('-----------------------------------', fg='white', err=False, nl=True)
        click.secho(message, fg='red', err=True, nl=True)
        click.secho('-----------------------------------', fg='white', err=False, nl=True)


def custom_print_table(tables, _headers, err=False):
    custom_print(tabulate(tables, _headers, tablefmt="grid", stralign="center", showindex=True))


class Printer(object):

    def table_to_be_printed(self):
        raise NotImplementedError("Please Implement this method")

    def print_response(self, before=None, after=None):
        if self.table_to_be_printed():
            custom_print_table(self.tables, self.headers)
        else:
            custom_print(self.response.content.decode('utf-8'))
