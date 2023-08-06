# type: ignore[attr-defined]

from typing import List, Optional, Tuple

import json
import os
import uuid

import typer
from arachnys_api_client import __version__
from arachnys_api_client.client import APIClient

INDENT = 2

app = typer.Typer(
    name="arachnys-api-client",
    help="API client for Arachnys APIs, including Unified Search, Entity API and others",
    add_completion=False,
)

user_id = os.getenv("ARACHNYS_PLATFORM_USER_ID")
secret_id = os.getenv("ARACHNYS_PLATFORM_SECRET_ID")
secret_key = os.getenv("ARACHNYS_PLATFORM_SECRET_KEY")
api_base = os.getenv(
    "ARACHNYS_PLATFORM_API_BASE", default="https://platform.arachnys.com/"
)

client = APIClient(
    user_id=user_id,
    secret_id=secret_id,
    secret_key=secret_key,
    api_base=api_base,
)


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        typer.secho(
            f"[yellow]arachnys-api-client[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="")
def main(
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the arachnys-api-client package.",
    ),
):
    pass


@app.command()
def get_access_token():
    token = client.refresh_token()
    typer.secho(f"Token is: %s" % token)
    raise typer.Exit()


@app.command()
def list_sources(
    query: Optional[str] = typer.Option(
        default=None,
        help="String to search for in source descriptions",
    ),
    category_ids: List[str] = typer.Option(
        default=(),
        help="Category ids",
    ),
    jurisdictions: List[str] = typer.Option(
        default=(),
        help="Jurisdictions (iso code)",
    ),
    return_attribute_ids: List[str] = typer.Option(
        default=(),
        help="Return attributes",
    ),
):
    sources = client.sources(
        query=query,
        category_ids=category_ids,
        jurisdictions=jurisdictions,
        return_attribute_ids=return_attribute_ids,
    )
    typer.secho(json.dumps(sources, indent=INDENT))


@app.command()
def get_source(id: str):
    source = client.sources(id=id)
    typer.secho(json.dumps(source, indent=INDENT))


@app.command()
def search_uss(
    source_ids: Optional[List[str]] = typer.Option(
        default=None,
        help="Source ID(s) to search",
    ),
    filter: Optional[str] = typer.Option(default=None, help="Filter JSON"),
):
    filter = json.loads(filter)
    search_page: SearchPage = client.search(
        source_ids=source_ids,
        filter=filter,
    )
    typer.secho(json.dumps(search_page.as_dict(), indent=INDENT))


@app.command()
def paginate_uss_search(
    search_id: Optional[str] = typer.Option(default=None),
    cursor: Optional[str] = typer.Option(default=None),
):
    response_dict: SearchPage = client.paginate_search(
        cursor=cursor,
        search_id=search_id,
    )
    typer.secho(json.dumps(response_dict.as_dict(), indent=INDENT))


@app.command()
def get_search_result(
    search_id: str = typer.Option(...),
    result_id: str = typer.Option(...),
):
    typer.secho(
        json.dumps(
            client.get_result_details(
                search_id=uuid.UUID(search_id),
                result_id=result_id,
            ).as_dict(),
            indent=INDENT,
        )
    )


@app.command()
def get_document(
    search_id: str = typer.Option(...),
    result_id: str = typer.Option(...),
    document_id: str = typer.Option(...),
):
    typer.secho(
        client.get_document(
            search_id=search_id,
            result_id=result_id,
            document_id=document_id,
        ).content
    )


if __name__ == "__main__":
    app()
