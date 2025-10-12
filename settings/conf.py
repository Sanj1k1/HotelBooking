#Project Modules
from decouple import config
# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)

ENV_ID = config("HOTELBOOKING_ENV_ID",cast=str)
SECRET_KEY = 'django-insecure-w_z5f9a*^afbjke7vg%9s6cw4-gjq%@98r2_($-$^df&totlf6'

