from flask import Flask, render_template, request

from models import db, Article, Comment


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy mit der App initialisieren
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Erstellt die Datenbank und Tabellen, wenn sie nicht existieren
        seed_database()


    @app.route('/')
    def index():
        articles: list[Article] = Article.query.all()
        return render_template('index.html', articles=articles)

    # Detailansicht eines Artikels
    @app.route('/article/<int:id>')
    def article_detail(id: int):
        article: Article = Article.query.get_or_404(id)
        return render_template('partials/article_detail.html', article=article)

    # Route zum Hinzufügen eines Kommentars (z. B. via htmx)
    @app.route('/comments', methods=['POST'])
    def add_comment():
        article_id: int = int(request.form.get('article_id'))
        text: str = request.form.get('text')
        user: str = request.form.get('user', 'Anonymous')

        if not article_id or not text:
            return "Fehlende Daten", 400

        comment = Comment(text=text, user=user, article_id=article_id)
        db.session.add(comment)
        db.session.commit()

        article = Article.query.get_or_404(article_id)
        return render_template('partials/comments.html', comments=article.comments)

    return app

def seed_database():
    # Prüfen, ob bereits Artikel existieren (damit seed-Daten nicht mehrfach eingefügt werden)
    if Article.query.first():
        print("Datenbank wurde bereits befüllt.")
        return

    # Erstellen einiger Artikel mit sinnvollen Inhalten und Kategorien
    article1 = Article(
        title="Bundespolitik im Wandel",
        summary="Ein Überblick über die aktuellen Entwicklungen in der Bundespolitik.",
        content="In diesem Artikel werden die neuesten Trends und Veränderungen in der politischen Landschaft Deutschlands detailliert erläutert...",
        category="Politik"
    )
    article2 = Article(
        title="Sportliche Höchstleistungen",
        summary="Ein Rückblick auf beeindruckende sportliche Erfolge dieser Saison.",
        content="Der Artikel beleuchtet die Höhepunkte der letzten Spiele und die herausragenden Leistungen einzelner Athleten...",
        category="Sport"
    )
    article3 = Article(
        title="Kulturelle Highlights des Jahres",
        summary="Ein Überblick über wichtige kulturelle Ereignisse und Ausstellungen.",
        content="Dieser Beitrag gibt einen Einblick in die innovativen kulturellen Projekte und Festivals, die das Jahr geprägt haben...",
        category="Kultur"
    )
    article4 = Article(
        title="Wirtschaftliche Perspektiven im Fokus",
        summary="Analyse der aktuellen Wirtschaftsdaten und Zukunftsaussichten.",
        content="Detaillierte Betrachtungen zu den wirtschaftlichen Entwicklungen, prognostizierten Trends und den Auswirkungen auf die Märkte...",
        category="Wirtschaft"
    )

    # Hinzufügen der Artikel zur Session
    db.session.add_all([article1, article2, article3, article4])
    db.session.commit()  # Commit, damit die Artikel IDs erhalten

    # Erstellen von Kommentaren, die den Artikeln zugeordnet werden
    comment1 = Comment(user="Max", text="Spannender Artikel – ich finde den politischen Wandel sehr interessant!", article_id=article1.id)
    comment2 = Comment(user="Julia", text="Ein sehr kritischer Blick, gefällt mir.", article_id=article1.id)
    comment3 = Comment(user="Tom", text="Tolles Spiel und beeindruckende Leistungen!", article_id=article2.id)
    comment4 = Comment(user="Lisa", text="Kulturell sehr bereichernd – tolle Zusammenfassung.", article_id=article3.id)
    comment5 = Comment(user="Anna", text="Gute Einblicke in die wirtschaftlichen Trends.", article_id=article4.id)
    comment6 = Comment(user="Markus", text="Ich freue mich auf weitere Artikel zu diesem Thema.", article_id=article4.id)

    # Hinzufügen der Kommentare zur Session
    db.session.add_all([comment1, comment2, comment3, comment4, comment5, comment6])
    db.session.commit()

    print("Datenbank erfolgreich befüllt!")

if __name__ == '__main__':
    app = create_app()
    app.run()
