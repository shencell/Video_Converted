# wsgi.py
from video_converter.backend.main import app

if __name__ == "__main__":
    app.run()