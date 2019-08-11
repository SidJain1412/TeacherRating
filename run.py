# Run this file to start the server. It uses the 'app' folder as a package
# (through app's __init__.py file)
from app import app


if(__name__ == "__main__"):
    app.run(debug=True)
