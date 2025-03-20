from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # Beziehung zu Kommentaren: Ein Artikel hat mehrere Kommentare
    comments = db.relationship('Comment', backref='article', lazy=True) # lazy=True bedeutet, dass die Kommentare erst geladen werden, wenn sie benötigt werden

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), default="Anonymous")
    text = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False) # Fremdschlüssel zu articles