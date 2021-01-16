import os
from src import app

if __name__ == "__main__":
    try:
        app.secret_key = os.urandom(12)
        app.run(debug=True, port=9000)
    except Exception as e:
        print(e)