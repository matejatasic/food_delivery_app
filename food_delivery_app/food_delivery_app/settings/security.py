import sys

CSP_IMG_SRC = ("'self'", "data:", "https://tile.openstreetmap.org", "https://unpkg.com")
CSP_STYLE_SRC = ("'self'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://unpkg.com")
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdn.jsdelivr.net",
    "https://code.jquery.com",
    "https://cdnjs.cloudflare.com",
    "https://js.stripe.com",
    "https://unpkg.com"
)
CSP_FONT_SRC = ("'self'", "https://cdn.jsdelivr.net")
CSP_FRAME_SRC = "https://js.stripe.com"
CSP_INCLUDE_NONCE_IN = ["script-src"]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 86400
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

AUTHENTICATION_BACKENDS = ["food_delivery_app.backend.UserModelBackend"]

if "test" in sys.argv:
    SECURE_SSL_REDIRECT = False
