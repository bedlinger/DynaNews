from flask import Flask, render_template

from models import db, Article, Comment


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy mit der App initialisieren
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Erstellt die Datenbank und Tabellen, wenn sie nicht existieren
        # db mit daten füllen
        if not Article.query.first():
            db.session.add_all([
                Article(title='Test', summary='Test', content='Test', category='Test'),
                Comment(user='Test', text='Test', article_id=1)
            ])
            db.session.commit()

    @app.route('/')
    def index():
        articels = Article.query.all()
        for a in articels:
            print(a.title)
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
