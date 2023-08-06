__all__ = ['patients', 'doctors', 'app']

import typer
from davidoc.apps.users import patients
from davidoc.apps.users import doctors


app = typer.Typer()

app.add_typer(patients.app, name='patient')

app.add_typer(doctors.app, name='doctor')



if __name__ == '__main__':
    typer.run(app)