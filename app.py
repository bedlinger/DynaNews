from flask import Flask, render_template

from models import db

app = Flask(__name__)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all() # Erstellt die Datenbank und Tabellen, wenn sie nicht existieren

    return app

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app = create_app()
    app.run()
