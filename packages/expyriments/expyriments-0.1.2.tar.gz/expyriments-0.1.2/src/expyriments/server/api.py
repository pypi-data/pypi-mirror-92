import json
import logging
import os
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from expyriments.server.api_utils import patch_fastapi

from . import config


@lru_cache()
def get_settings() -> config.Settings:
    return config.Settings()


class Host(BaseModel):
    hostname: str
    os: str
    cpu: str
    cpuCores: str
    memorySize: str
    pythonVersion: str
    pythonCompiler: str
    pythonImpl: str
    workspaceVersion: str = ""
    gpus: List[str]


class ExpyrimentResources(BaseModel):
    input: List[str]
    artifacts: List[str]
    experimentDir: str
    sourceScript: str
    stdout: str


class Expyriment(BaseModel):
    key: str
    name: str
    operator: str
    scriptName: str
    scriptType: str
    project: str
    startedAt: int
    finishedAt: int
    updatedAt: int
    duration: int
    status: str
    command: str
    clientVersion: str
    git: Dict[str, str] = {}
    host: Host
    dependencies: List[str] = []
    resources: ExpyrimentResources
    # Todo: Check if dedicated model should be used
    parameters: Dict[str, float] = {}
    metrics: Dict[str, float] = {}
    others: dict = {}
    result: str


def get_webapp_path() -> str:
    # Todo: Refactor after decision on how to handle generated react app
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static_webapp")


app = FastAPI(
    title="Expyriments Dashboard",
    description="Organize, run, track and share experiments & data.",
)

api_app = FastAPI(
    title="Expyriments API",
    description="Organize, run, track and share experiments & data.",
)


@api_app.get("/expyriments/{key}", response_model=Expyriment)
def read_expyriment(
    key: str, settings: config.Settings = Depends(get_settings)
) -> Expyriment:
    """Read a single expyriment by key.

    Args:
        key (str): Expyriment key
        settings (config.Settings, optional): App Settings.

    Raises:
        HTTPException: If not expyriment found for given key.

    Returns:
        Expyriment: The expyriment
    """
    logging.info(f"Read expyriment {key}")
    expyriments = match_expyriments(settings, _match_by_key, {"key": key})
    if expyriments:
        count = len(expyriments)
        if count > 1:
            logging.warning(f"{count} expyriments found for key {key}.")
            logging.debug(f"Return only the first expyriment of {count} for key {key}")
        return expyriments[0]
    raise HTTPException(status_code=404, detail=f"Expyriment {key} not found")


@api_app.get("/expyriments", response_model=List[Expyriment])
def read_expyriments(
    project: Optional[str] = None, settings: config.Settings = Depends(get_settings)
) -> List[Expyriment]:
    """Read multiple expyriments.

    Args:
        project (Optional[str], optional): The project identifier. Defaults to None.
        settings (config.Settings, optional): App settings.

    Returns:
        List[Expyriment]: List with expyriments.
    """
    logging.info(f"Read expyriments for project {project}")

    if project:
        return match_expyriments(settings, _match_by_project, {"project": project})
    else:
        return match_expyriments(settings)


app.mount("/api", api_app)
webapp_endpoint_name = "webapp"
try:
    app.mount(
        "/",
        StaticFiles(directory=get_webapp_path(), html=True),
        name=webapp_endpoint_name,
    )
except RuntimeError as e:
    logging.error(
        f"An error occurred: {e}. The endpoint '{webapp_endpoint_name}' is not ready"
    )


def match_expyriments(
    settings: config.Settings,
    filter_fn: Callable[[Expyriment, Dict[str, Any]], bool] = None,
    filter_args: Optional[Dict[str, Any]] = None,
) -> List[Expyriment]:
    """Read expyriments and optionally filter the result set.

    Args:
        settings (config.Settings): App Settings
        filter_fn (Optional[Callable[[Expyriment, Dict[str, Any]], bool]], optional): Filter function.
        args (Optional[Dict[str, Any]], optional): Arguments that will be handed over to the filter function.

    Returns:
        List[Expyriment]: List with expyriments.
    """

    matched_expyriments: List[Expyriment] = []

    for dir_content in os.walk(settings.expyriment_dir):
        for file_name in dir_content[2]:

            if not file_name.endswith(settings.expyriment_file_suffix):
                continue

            file_path = os.path.join(dir_content[0], file_name)
            file = open(file_path, "r")
            try:
                file_content = json.load(file)
            except json.decoder.JSONDecodeError:
                logging.info(f"File {file_path} could not be parsed - skipped")
                continue

            if not is_valid_expyriment_json(file_content):
                logging.info(
                    f"The file {file_path} is skipped, because it does not contain valid expyriments json"
                )
                continue
            expyriment = Expyriment(**file_content)
            if not filter_fn or filter_args and filter_fn(expyriment, filter_args):
                matched_expyriments.append(expyriment)

    return matched_expyriments


def is_valid_expyriment_json(json_data: dict) -> bool:
    return "key" in json_data.keys()


def _match_by_key(expyriment: Expyriment, args: Dict[str, str]) -> bool:
    return expyriment.key == args["key"]


def _match_by_project(expyriment: Expyriment, args: Dict[str, str]) -> bool:
    return expyriment.project == args["project"]


# Patch Fastapi to allow relative path resolution.
patch_fastapi(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=8081, log_level="info"
    )  # cannot use reload=True anymore
