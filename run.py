"""Run the Flask application."""
import webbrowser
import threading
import time
from app import create_app

app = create_app()

def open_browser():
    """Open the browser after a short delay to ensure the server is running."""
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Start a thread to open the browser
    threading.Thread(target=open_browser).start()
    # Run the Flask application
    app.run(debug=True)
