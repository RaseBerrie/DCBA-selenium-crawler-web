from main import app

import logging
logging.basicConfig(filename="logs/flask_error.log", level=logging.ERROR)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)