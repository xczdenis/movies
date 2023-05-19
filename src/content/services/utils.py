import json


async def make_key_from_args(**kwargs) -> str:
    for k, v in kwargs.items():
        if hasattr(v, "__name__"):
            kwargs[k] = v.__name__
        kwargs[k] = str(kwargs[k])
    return f"{json.dumps({'kwargs': kwargs}, sort_keys=True)}"
