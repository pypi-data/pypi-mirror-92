import typer
from davidoc.apps.services import prescriptions
from davidoc.apps.services import visits

app = typer.Typer()

app.add_typer(prescriptions.app, name='rx')
app.add_typer(visits.app, name='visit')


if __name__ == '__main__':
    typer.run(app())