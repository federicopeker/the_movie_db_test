import os

from flask import send_from_directory

from app import create_app

app = create_app()


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("../static", path)


if __name__ == "__main__":
    debug_mode = os.getenv("TMDB_FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode)
