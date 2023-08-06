import typer

app = typer.Typer(name='visit')


@app.command()
def init(patient: str):
    typer.echo(f"Starting visit for: {patient}")


@app.command()
def save(patient: str):
    typer.echo(f"Finishing and saving visit for: {patient}")


@app.callback()
def main(ctx: typer.Context):
    """
    Manage visits in the CLI DocApp.
    """
    typer.echo(f"About to execute command: {ctx.invoked_subcommand}")
    return ctx.obj



if __name__ == '__main__':
    app()