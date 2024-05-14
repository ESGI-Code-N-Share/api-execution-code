from flask import Flask
from routes.execute_code_routes import configure_routes

app = Flask(__name__)
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
