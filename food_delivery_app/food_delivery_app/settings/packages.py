from .base import os

BING_MAPS_API_KEY=os.getenv("BING_MAPS_API_KEY")

CRISPY_TEMPLATE_PACK = 'bootstrap5'

INTERNAL_IPS = os.getenv("ALLOWED_HOSTS", default="127.0.0.1").split(" ")

SELECT2_CACHE_BACKEND = "select2"