import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from models import db, Article, Comment


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialisiert die Datenbank mit der Flask-App
    with app.app_context():
        if os.environ.get('IS_DEVELOPMENT') == 'TRUE':  # Entwicklungsmodus
            db.drop_all()  # Löscht alle Tabellen in der Datenbank
            db.create_all()  # Erstellt alle Tabellen in der Datenbank
            seed_database()  # Seed-Daten in die Datenbank einfügen
        else:
            db.create_all()

    @app.route('/')
    def index():
        articles: list[Article] = Article.query.all()
        return render_template('index.html', articles=articles)

    # Detailansicht eines Artikels
    @app.route('/article/<int:id>')
    def article_detail(id: int):
        article: Article = Article.query.get_or_404(id)
        return render_template('partials/article_detail.html', article=article)

    # Route zum Hinzufügen eines Kommentars
    @app.route('/comments', methods=['POST'])
    def add_comment():
        article_id: int = int(request.form.get('article_id'))
        text: str = request.form.get('text')
        user: str = request.form.get('user', 'Anonymous')

        if not article_id or not text:
            return 'Fehlende Daten', 400

        comment = Comment(text=text, user=user, article_id=article_id)
        db.session.add(comment)
        db.session.commit()

        article = Article.query.get_or_404(article_id)
        return render_template('partials/comments.html', comments=article.comments)

    return app


def seed_database():
    # Prüfen, ob bereits Artikel existieren (damit seed-Daten nicht mehrfach eingefügt werden)
    if Article.query.first():
        print('Datenbank wurde bereits befüllt.')
        return

    # Erstellen vieler Artikel mit verschiedenen Kategorien
    articles = [Article(
        title='Bundespolitik im Wandel',
        summary='Ein Überblick über die aktuellen Entwicklungen in der Bundespolitik.',
        content='In diesem Artikel werden die neuesten Trends und Veränderungen in der politischen Landschaft Deutschlands detailliert erläutert...',
        category='Politik'
    ), Article(
        title='Neue Gesetzesinitiative vorgestellt',
        summary='Die Regierung hat eine neue Initiative zum Klimaschutz angekündigt.',
        content='Die gestern vorgestellte Gesetzesinitiative sieht umfassende Änderungen im Bereich der Umweltpolitik vor...',
        category='Politik'
    ), Article(
        title='Wahlergebnisse analysiert',
        summary='Experten bewerten die jüngsten politischen Entwicklungen.',
        content='Nach den Landtagswahlen zeichnen sich neue Koalitionsmöglichkeiten ab, die das politische Gefüge verändern könnten...',
        category='Politik'
    ), Article(
        title='Sportliche Höchstleistungen',
        summary='Ein Rückblick auf beeindruckende sportliche Erfolge dieser Saison.',
        content='Der Artikel beleuchtet die Höhepunkte der letzten Spiele und die herausragenden Leistungen einzelner Athleten...',
        category='Sport'
    ), Article(
        title='Überraschender Sieg im Finale',
        summary='Außenseiter gewinnt das wichtigste Turnier des Jahres.',
        content='In einem spannenden Finale setzte sich der Underdog gegen den haushohen Favoriten durch...',
        category='Sport'
    ), Article(
        title='Neuer Transferrekord aufgestellt',
        summary='Fußballverein zahlt Rekordsumme für Stürmertalent.',
        content='Der Transfer übertrifft alle bisherigen Rekorde und setzt neue Maßstäbe auf dem Transfermarkt...',
        category='Sport'
    ), Article(
        title='Kulturelle Highlights des Jahres',
        summary='Ein Überblick über wichtige kulturelle Ereignisse und Ausstellungen.',
        content='Dieser Beitrag gibt einen Einblick in die innovativen kulturellen Projekte und Festivals, die das Jahr geprägt haben...',
        category='Kultur'
    ), Article(
        title='Neuer Kinofilm bricht alle Rekorde',
        summary='Der langerwartete Blockbuster übertrifft alle Erwartungen.',
        content='Mit beeindruckenden Effekten und einer fesselnden Story zieht der Film weltweit Millionen von Zuschauern in die Kinos...',
        category='Kultur'
    ), Article(
        title='Wirtschaftliche Perspektiven im Fokus',
        summary='Analyse der aktuellen Wirtschaftsdaten und Zukunftsaussichten.',
        content='Detaillierte Betrachtungen zu den wirtschaftlichen Entwicklungen, prognostizierten Trends und den Auswirkungen auf die Märkte...',
        category='Wirtschaft'
    ), Article(
        title='Tech-Unternehmen auf Rekordkurs',
        summary='Börsennotierte Technologieunternehmen verzeichnen starkes Wachstum.',
        content='Trotz globaler Herausforderungen wachsen die Gewinne der führenden Tech-Konzerne weiter...',
        category='Wirtschaft'
    ), Article(
        title='KI-Revolution in der Industrie',
        summary='Wie künstliche Intelligenz die Produktion verändert.',
        content='Immer mehr Unternehmen setzen auf KI-gestützte Prozesse, um Effizienz und Qualität zu steigern...',
        category='Technologie'
    ), Article(
        title='Neue Smartphone-Generation vorgestellt',
        summary='Die neuesten Modelle überraschen mit innovativen Funktionen.',
        content='Die heute präsentierten Geräte verfügen über verbesserte Kameras und längere Akkulaufzeiten...',
        category='Technologie'
    ), Article(
        title='Durchbruch in der Quantenphysik',
        summary='Forscher erzielen bahnbrechende Ergebnisse bei Quantenexperimenten.',
        content='Das internationale Forschungsteam hat einen Weg gefunden, Quantenzustände länger stabil zu halten...',
        category='Wissenschaft'
    ), Article(
        title='Neue Erkenntnisse zur gesunden Ernährung',
        summary='Studie zeigt Zusammenhang zwischen Ernährung und Wohlbefinden.',
        content='Die Langzeitstudie belegt den positiven Einfluss einer ausgewogenen Ernährung auf verschiedene Gesundheitsaspekte...',
        category='Gesundheit'
    ), Article(
        title='Fortschritte beim Klimaschutz',
        summary='Neue Maßnahmen zeigen erste positive Auswirkungen.',
        content='Die in den letzten Jahren eingeleiteten Klimaschutzprojekte führen zu messbaren Verbesserungen...',
        category='Umwelt'
    )]

    # Hinzufügen der Artikel zur Session
    db.session.add_all(articles)
    db.session.commit()  # Commit, damit die Artikel IDs erhalten

    # Benutzernamen für Kommentare
    users = ['Max', 'Julia', 'Tom', 'Lisa', 'Anna', 'Markus', 'Sophie', 'Paul',
             'Laura', 'David', 'Emma', 'Felix', 'Sarah', 'Michael', 'Lena', 'Jonas']

    # Kommentar-Templates
    comment_templates = [
        'Sehr informativer Artikel! Danke für die Einblicke.',
        'Ich stimme dem Artikel nicht ganz zu. Meiner Meinung nach...',
        'Toller Beitrag, hat mir neue Perspektiven eröffnet.',
        'Interessantes Thema, würde gerne mehr darüber lesen.',
        'Danke für die detaillierte Analyse!',
        'Die Fakten in diesem Artikel sind sehr aufschlussreich.',
        'Ein gut geschriebener Artikel zu einem wichtigen Thema.',
        'Ich verfolge dieses Thema schon länger und finde den Artikel sehr treffend.',
        'Beeindruckende Recherche zu diesem komplexen Thema.',
        'Der Artikel hat mich zum Nachdenken angeregt.',
        'Ich freue mich auf weitere Artikel zu diesem Thema.',
        'Gut strukturierter Beitrag mit wertvollen Informationen.',
        'Die dargestellten Zusammenhänge waren mir so nicht bewusst.',
        'Sehr aktuelle Berichterstattung, vielen Dank!'
    ]

    comments = []
    import random

    # Für jeden Artikel mindestens 2-5 Kommentare erstellen
    for article in articles:
        num_comments = random.randint(2, 5)
        for _ in range(num_comments):
            user = random.choice(users)
            comment_text = random.choice(comment_templates)
            comments.append(Comment(
                user=user,
                text=comment_text,
                article_id=article.id
            ))

    # Spezielle Kommentare für einige Artikel
    comments.extend([
        Comment(user='Max', text='Spannender Artikel – ich finde den politischen Wandel sehr interessant!',
                article_id=articles[0].id),
        Comment(user='Julia', text='Ein sehr kritischer Blick, gefällt mir.', article_id=articles[0].id),
        Comment(user='Tom', text='Tolles Spiel und beeindruckende Leistungen!', article_id=articles[3].id),
        Comment(user='Lisa', text='Kulturell sehr bereichernd – tolle Zusammenfassung.', article_id=articles[6].id),
        Comment(user='Anna', text='Gute Einblicke in die wirtschaftlichen Trends.', article_id=articles[8].id),
        Comment(user='Markus', text='Technologische Entwicklungen beeinflussen unseren Alltag immer stärker.',
                article_id=articles[10].id)
    ])

    # Hinzufügen der Kommentare
    db.session.add_all(comments)
    db.session.commit()

    print(f'Datenbank erfolgreich befüllt mit {len(articles)} Artikeln und {len(comments)} Kommentaren!')


if __name__ == '__main__':
    app = create_app()
    app.run()
