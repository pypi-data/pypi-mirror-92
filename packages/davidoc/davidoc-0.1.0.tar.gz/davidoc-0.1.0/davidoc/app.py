#!/usr/bin/env python
# -*- utf-8 -*-
import datetime
import typer
from sqlalchemy.orm import Session
from davidoc.apps.users import main as user
from davidoc.apps.services import main as service
from davidoc.apps.utils import main as util
from davidoc.core.db import get_db
from davidoc.core import orm




doc = typer.Typer(name='doc')
doc.add_typer(user.app, name='user')
doc.add_typer(service.app, name='service')
doc.add_typer(util.app, name='util')

@doc.command()
def visit(patient_id:int):
    db: Session = next(get_db())
    patient = db.query(orm.Patient).filter(orm.Patient.id == patient_id).first()
    if patient:
        typer.secho(message=f'O paciente {patient} foi selecionado para a visita.')
    else:
        typer.secho(message=f'Nenhum paciente foi encontrado com o id {patient_id}')




@doc.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage documents for smart doctors using CLI DocApp.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Initializing database")
        next(get_db())



if __name__ == '__main__':
    doc()