import os
from random import shuffle

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

        if not article_id:
            return 'Article ID is required', 400
        if not text:
            return 'Comment text is required', 400

        comment = Comment(text=text, user=user, article_id=article_id)
        db.session.add(comment)
        db.session.commit()

        article = Article.query.get_or_404(article_id)
        return render_template('partials/comments.html', comments=article.comments)

    return app


def seed_database():
    # Prüfen, ob bereits Artikel existieren (damit Seed-Daten nicht mehrfach eingefügt werden)
    if Article.query.first():
        print('Datenbank wurde bereits befüllt.')
        return

    articles = []

    # Artikel in der Kategorie "Politik"
    articles.extend([
        Article(
            title='Bundespolitik im Wandel',
            summary='Ein Überblick über die aktuellen Entwicklungen in der Bundespolitik.',
            content='In diesem Artikel werden die neuesten Trends und Veränderungen in der politischen Landschaft Deutschlands detailliert erläutert...',
            category='Politik'
        ),
        Article(
            title='Neue Gesetzesinitiative vorgestellt',
            summary='Die Regierung hat eine neue Initiative zum Klimaschutz angekündigt.',
            content='Die gestern vorgestellte Gesetzesinitiative sieht umfassende Änderungen im Bereich der Umweltpolitik vor...',
            category='Politik'
        ),
        Article(
            title='Wahlergebnisse analysiert',
            summary='Experten bewerten die jüngsten politischen Entwicklungen.',
            content='Nach den Landtagswahlen zeichnen sich neue Koalitionsmöglichkeiten ab, die das politische Gefüge verändern könnten...',
            category='Politik'
        ),
        Article(
            title='Die Zukunft der EU-Politik',
            summary='Ein Blick auf die zukünftige Ausrichtung der Europäischen Union.',
            content='Die EU steht vor großen Herausforderungen und Chancen, die sich in den kommenden Jahren manifestieren werden...',
            category='Politik'
        )
    ])

    # Artikel in der Kategorie "Sport"
    articles.extend([
        Article(
            title='Sportliche Höchstleistungen',
            summary='Ein Rückblick auf beeindruckende sportliche Erfolge dieser Saison.',
            content='Der Artikel beleuchtet die Höhepunkte der letzten Spiele und die herausragenden Leistungen einzelner Athleten...',
            category='Sport'
        ),
        Article(
            title='Überraschender Sieg im Finale',
            summary='Außenseiter gewinnt das wichtigste Turnier des Jahres.',
            content='In einem spannenden Finale setzte sich der Underdog gegen den haushohen Favoriten durch...',
            category='Sport'
        ),
        Article(
            title='Neuer Transferrekord aufgestellt',
            summary='Fußballverein zahlt Rekordsumme für Stürmertalent.',
            content='Der Transfer übertrifft alle bisherigen Rekorde und setzt neue Maßstäbe auf dem Transfermarkt...',
            category='Sport'
        ),
        Article(
            title='Olympische Spiele: Erwartungen und Prognosen',
            summary='Ein Ausblick auf die kommenden Olympischen Spiele und die Favoriten in verschiedenen Disziplinen.',
            content='Experten diskutieren, welche Nationen und Athleten im Rennen um Medaillen stehen und welche Überraschungen möglich sind...',
            category='Sport'
        )
    ])

    # Artikel in der Kategorie "Kultur"
    articles.extend([
        Article(
            title='Kulturelle Highlights des Jahres',
            summary='Ein Überblick über wichtige kulturelle Ereignisse und Ausstellungen.',
            content='Dieser Beitrag gibt einen Einblick in die innovativen kulturellen Projekte und Festivals, die das Jahr geprägt haben...',
            category='Kultur'
        ),
        Article(
            title='Neuer Kinofilm bricht alle Rekorde',
            summary='Der langerwartete Blockbuster übertrifft alle Erwartungen.',
            content='Mit beeindruckenden Effekten und einer fesselnden Story zieht der Film weltweit Millionen von Zuschauern in die Kinos...',
            category='Kultur'
        ),
        Article(
            title='Kunstinstallation erobert die Stadt',
            summary='Eine innovative Kunstinstallation verwandelt den öffentlichen Raum.',
            content='Die Installation hat zahlreiche Besucher und Kritiker gleichermaßen begeistert und regt zu Diskussionen an...',
            category='Kultur'
        )
    ])

    # Artikel in der Kategorie "Wirtschaft"
    articles.extend([
        Article(
            title='Wirtschaftliche Perspektiven im Fokus',
            summary='Analyse der aktuellen Wirtschaftsdaten und Zukunftsaussichten.',
            content='Detaillierte Betrachtungen zu den wirtschaftlichen Entwicklungen, prognostizierten Trends und den Auswirkungen auf die Märkte...',
            category='Wirtschaft'
        ),
        Article(
            title='Tech-Unternehmen auf Rekordkurs',
            summary='Börsennotierte Technologieunternehmen verzeichnen starkes Wachstum.',
            content='Trotz globaler Herausforderungen wachsen die Gewinne der führenden Tech-Konzerne weiter...',
            category='Wirtschaft'
        ),
        Article(
            title='Start-up-Szene boomt',
            summary='Innovative Gründer verändern die Wirtschaft mit disruptiven Ideen.',
            content='Immer mehr Start-ups sichern sich internationale Investitionen und stellen traditionelle Geschäftsmodelle in Frage...',
            category='Wirtschaft'
        )
    ])

    # Artikel in der Kategorie "Technologie"
    articles.extend([
        Article(
            title='KI-Revolution in der Industrie',
            summary='Wie künstliche Intelligenz die Produktion verändert.',
            content='Immer mehr Unternehmen setzen auf KI-gestützte Prozesse, um Effizienz und Qualität zu steigern...',
            category='Technologie'
        ),
        Article(
            title='Neue Smartphone-Generation vorgestellt',
            summary='Die neuesten Modelle überraschen mit innovativen Funktionen.',
            content='Die heute präsentierten Geräte verfügen über verbesserte Kameras und längere Akkulaufzeiten...',
            category='Technologie'
        ),
        Article(
            title='Cybersecurity im Fokus',
            summary='Unternehmen investieren verstärkt in digitale Sicherheit.',
            content='Angesichts zunehmender Cyberangriffe setzen Firmen verstärkt auf moderne Sicherheitslösungen...',
            category='Technologie'
        )
    ])

    # Artikel in der Kategorie "Wissenschaft"
    articles.extend([
        Article(
            title='Durchbruch in der Quantenphysik',
            summary='Forscher erzielen bahnbrechende Ergebnisse bei Quantenexperimenten.',
            content='Das internationale Forschungsteam hat einen Weg gefunden, Quantenzustände länger stabil zu halten...',
            category='Wissenschaft'
        ),
        Article(
            title='Neue Entdeckungen im Weltall',
            summary='Astronomen entdecken einen bislang unbekannten Planeten außerhalb unseres Sonnensystems.',
            content='Die Beobachtungen deuten auf die Existenz eines erdähnlichen Planeten hin, der möglicherweise Leben beherbergen könnte...',
            category='Wissenschaft'
        )
    ])

    # Artikel in der Kategorie "Gesundheit"
    articles.extend([
        Article(
            title='Neue Erkenntnisse zur gesunden Ernährung',
            summary='Studie zeigt Zusammenhang zwischen Ernährung und Wohlbefinden.',
            content='Die Langzeitstudie belegt den positiven Einfluss einer ausgewogenen Ernährung auf verschiedene Gesundheitsaspekte...',
            category='Gesundheit'
        ),
        Article(
            title='Innovationen in der Medizintechnik',
            summary='Moderne Technologien revolutionieren die Patientenversorgung.',
            content='Neue medizinische Geräte und Verfahren verbessern die Diagnostik und Behandlung von Krankheiten signifikant...',
            category='Gesundheit'
        )
    ])

    # Artikel in der Kategorie "Umwelt"
    articles.extend([
        Article(
            title='Fortschritte beim Klimaschutz',
            summary='Neue Maßnahmen zeigen erste positive Auswirkungen.',
            content='Die in den letzten Jahren eingeleiteten Klimaschutzprojekte führen zu messbaren Verbesserungen...',
            category='Umwelt'
        ),
        Article(
            title='Nachhaltige Energiequellen im Aufschwung',
            summary='Erneuerbare Energien gewinnen an Bedeutung.',
            content='Investitionen in Solar-, Wind- und Wasserkraftanlagen nehmen weltweit zu und verändern die Energiebranche...',
            category='Umwelt'
        )
    ])

    # Artikel in der neuen Kategorie "Reisen"
    articles.extend([
        Article(
            title='Abenteuerliche Reisen in ferne Länder',
            summary='Ein Reiseführer zu den exotischsten Destinationen.',
            content='Von den unberührten Stränden Südostasiens bis zu den historischen Stätten Europas – entdecken Sie die Welt neu...',
            category='Reisen'
        ),
        Article(
            title='Städtereisen: Kultur und Genuss',
            summary='Die besten Städte für Kurztrips und kulinarische Highlights.',
            content='Einblicke in das pulsierende Stadtleben, historische Architektur und lokale Spezialitäten machen jede Städtereise unvergesslich...',
            category='Reisen'
        )
    ])

    # Artikel zur Datenbank hinzufügen und committen
    shuffle(articles)
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

    # Für jeden Artikel 2-5 zufällige Kommentare generieren
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

    # Spezielle Kommentare für ausgewählte Artikel
    special_comments = [
        Comment(user='Max', text='Spannender Artikel – ich finde den politischen Wandel sehr interessant!',
                article_id=articles[0].id),
        Comment(user='Julia', text='Ein sehr kritischer Blick, gefällt mir.', article_id=articles[0].id),
        Comment(user='Tom', text='Tolles Spiel und beeindruckende Leistungen!', article_id=articles[4].id),
        Comment(user='Lisa', text='Kulturell sehr bereichernd – tolle Zusammenfassung.', article_id=articles[6].id),
        Comment(user='Anna', text='Gute Einblicke in die wirtschaftlichen Trends.', article_id=articles[8].id),
        Comment(user='Markus', text='Technologische Entwicklungen beeinflussen unseren Alltag immer stärker.',
                article_id=articles[10].id)
    ]
    comments.extend(special_comments)

    # Kommentare zur Datenbank hinzufügen und committen
    db.session.add_all(comments)
    db.session.commit()

    print(f'Datenbank erfolgreich befüllt mit {len(articles)} Artikeln und {len(comments)} Kommentaren!')


if __name__ == '__main__':
    app = create_app()
    app.run()
