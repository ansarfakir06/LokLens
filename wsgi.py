"""
LokLens — Production WSGI Entry Point (wsgi.py)

Usage for Production Deployment:
- Linux / Cloud (Render, Railway, Heroku): gunicorn wsgi:app
- Windows / Cross-platform: waitress-serve --port=5000 wsgi:app
"""

from app import app

if __name__ == "__main__":
    app.run()
