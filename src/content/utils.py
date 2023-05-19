from typing import Any

from fastapi import FastAPI


def get_all_sub_apps(app: FastAPI) -> list[FastAPI]:
    return [route.app for route in app.routes if hasattr(route, "app") and isinstance(route.app, FastAPI)]


def case_free_pop(data: dict, key: Any, default_value: Any | None = None):
    if isinstance(key, str):
        for k in (key, key.upper(), key.lower()):
            if k in data:
                return data.pop(k)
    else:
        if key in data:
            return data.pop(key)
    return default_value
