" flask backend application for managing trips "
from flask import Flask
import db
from routes.trips import trips_bp
from routes.places import places_bp
from routes.notes import notes_bp
from routes.expenses import expenses_bp
from routes.analytics import analytics_bp

app = Flask(__name__)
db.init_db()

app.register_blueprint(trips_bp)
app.register_blueprint(places_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run(debug=True)
