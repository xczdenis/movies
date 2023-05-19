from split_settings.tools import include, optional

from adminpanel.config.settings.components import app_settings

_base_settings = (
    "components/base.py",
    "components/database.py",
    "components/drf.py",
    # Select the right env:
    "environments/{0}.py".format(app_settings.ENVIRONMENT),
    # Optionally override some settings:
    optional("environments/local.py"),
)

include(*_base_settings)
