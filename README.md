# DynaNews

A dynamic news web application built with Flask and HTMX. Browse, search, and filter news articles across multiple categories, and leave comments — all without full page reloads.

## Motivation

This project was built as a hands-on way to learn [HTMX](https://htmx.org/) and put it into practice by building something real. The goal was to explore how HTMX enables dynamic, interactive web experiences with minimal JavaScript, using server-rendered HTML partials instead.

## Features

- **Browse articles** organized by categories (Politics, Sport, Culture, Economy, Technology, Science, Health, Environment, Travel)
- **Search** across article titles, summaries, and content
- **Filter** articles by category
- **Pagination** – load more articles on demand
- **Article detail view** – opened in a modal without leaving the page
- **Comments** – add and view comments per article
- **Development mode** – automatically seeds the database with sample articles and comments

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | Python · Flask · SQLAlchemy (SQLite)    |
| Frontend  | HTMX · DaisyUI · Tailwind CSS · Material Icons |

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/bedlinger/DynaNews.git
   cd DynaNews
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install flask flask-sqlalchemy python-dotenv
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   # Set to TRUE to reset and re-seed the database on every startup (development only)
   IS_DEVELOPMENT=TRUE
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

   The app will be available at `http://127.0.0.1:5000`.

## Project Structure

```
DynaNews/
├── app.py          # Application factory, routes, and database seeding
├── models.py       # SQLAlchemy models (Article, Comment)
├── templates/
│   ├── base.html           # HTML boilerplate with CDN assets
│   ├── layout.html         # Navigation header and content wrapper
│   ├── index.html          # Main page (search, filter, article grid)
│   └── partials/           # HTMX partial templates
│       ├── articles.html
│       ├── article_detail.html
│       └── comments.html
└── instance/
    └── news.db     # SQLite database (auto-created, git-ignored)
```

## Configuration

| Variable         | Default | Description                                                  |
|------------------|---------|--------------------------------------------------------------|
| `IS_DEVELOPMENT` | —       | Set to `TRUE` to drop and recreate the database on startup   |
