from pydantic import BaseSettings


class Settings(BaseSettings):
    expyriment_dir: str = "."
    expyriment_file_suffix = "_exp.json"
