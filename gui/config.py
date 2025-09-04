import os
from dotenv import load_dotenv

load_dotenv()  # reads .env if present

def server_defaults():
    """
    Returns a default connection values pulled from env if the program runs with
    docker.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "oma"),
    }
