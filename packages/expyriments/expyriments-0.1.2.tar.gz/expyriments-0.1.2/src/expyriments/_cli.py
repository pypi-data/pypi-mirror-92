"""Command line interface."""

import json

import typer

from expyriments import server

cli = typer.Typer()


@cli.command()
def hello(name: str) -> None:
    typer.echo(f"Hello {name}")


@cli.command()
def start_server(host: str = "0.0.0.0", port: int = 8081) -> None:
    import uvicorn

    typer.echo("Starting Expyriment Server ...")

    uvicorn.run(
        server.app, host=host, port=port, log_level="info"
    )  # cannot use reload=True anymore


@cli.command()
def generate_openapi_specs() -> None:
    # write openapi.json spec to file
    with open("./openapi.json", "w") as outfile:
        print("Create API docs", server.api_app.openapi())
        json.dump(server.api_app.openapi(), outfile)


if __name__ == "__main__":
    cli()
