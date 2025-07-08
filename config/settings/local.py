from config.settings.base import *


# Debug Toolbar config

USE_TOOLBAR = env("USE_TOOLBAR", default=False, cast=bool)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: USE_TOOLBAR
}
