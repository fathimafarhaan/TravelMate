" flask backend application for managing trips "
from flask import Flask
import db
from routes.trips import trips_bp

app = Flask(__name__)
db.init_db()

app.register_blueprint(trips_bp)

if __name__ == "__main__":
    app.run(debug=True)
