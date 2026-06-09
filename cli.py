import typer
from database import insert_record, retrieve_records

app = typer.Typer()

@app.command()
def add(data: str, password: str):
    insert_record("records.db", data, password)
    typer.echo("Record inserted.")

@app.command()
def fetch(password: str):
    records = retrieve_records("records.db", password)
    for record in records:
        typer.echo(record)

if __name__ == "__main__":
    app()