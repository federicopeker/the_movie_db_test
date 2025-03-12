import os

from app import create_app

app = create_app()


if __name__ == "__main__":
    debug_mode = os.getenv("TMDB_FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode)
