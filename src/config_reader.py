from functools import lru_cache
from pathlib import Path
from tomllib import load
from typing import Type, TypeVar

from pydantic import BaseModel, SecretStr

ConfigType = TypeVar("ConfigType", bound=BaseModel)


class AppConfig(BaseModel):
    bot_token: SecretStr
    gifts_dir: Path


@lru_cache
def parse_config_file() -> dict:
    with open("settings.toml", "rb") as file:
        config_data = load(file)
    return config_data


@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = parse_config_file()
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)
    return model.model_validate(config_dict[root_key])