import typer
import datetime
import asyncio

app = typer.Typer()

@app.command()
def today() -> datetime.date:
    rs = asyncio.run(a_today())
    typer.secho(message=f'O dia atual é {rs}', fg=typer.colors.YELLOW)
    return rs


@app.command()
def now() -> datetime.datetime:
    rs = asyncio.run(a_now())
    typer.secho(message=f'A data e hora atual é {rs}', fg=typer.colors.YELLOW)
    return rs


async def a_today() -> datetime.date:
    return datetime.date.today()


async def a_now() -> datetime.datetime:
    return datetime.datetime.now()