def make_rout_name(namespace: str, url_name: str) -> str:
    return "{namespace}:{url_name}".format(namespace=namespace, url_name=url_name)
