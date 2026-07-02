import os

from app import create_app
from app.config_factory import get_config_from_env

app = create_app(get_config_from_env())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

