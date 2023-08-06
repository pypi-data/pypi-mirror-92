import os

__version__ = "1.0.0"

SECRET_FOLDER = os.path.dirname(os.path.abspath(__file__) + '/secret')

SERVICE_ACCOUNT_FILE = '/auth.json'.format(SECRET_FOLDER)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
SERVICE_ACCOUNT_EMAIL = os.getenv('SERVICE_ACCOUNT_EMAIL', None)
SERVICE_NAME_AUDIENCE = os.getenv('SERVICE_NAME_AUDIENCE', None)

try:
    with open(SERVICE_ACCOUNT_FILE) as f:
        f.close()
except IOError:
    msg = "auth.json file or secret folder not found"
    raise SystemExit("Error: {}".format(msg))

if not GOOGLE_APPLICATION_CREDENTIALS:
    msg = "environment variable 'GOOGLE_APPLICATION_CREDENTIALS' not found"
    raise SystemExit("KeyError: {}".format(msg))
elif not SERVICE_ACCOUNT_EMAIL:
    msg = "environment variable 'SERVICE_ACCOUNT_EMAIL' not found"
    raise SystemExit("KeyError: {}".format(msg))
elif not SERVICE_NAME_AUDIENCE:
    msg = "environment variable 'SERVICE_NAME_AUDIENCE' not found"
    raise SystemExit("KeyError: {}".format(msg))
