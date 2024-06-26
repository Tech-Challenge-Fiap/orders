import os
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)

db_name = os.environ.get("POSTGRES_DB", "myappdb")
db_user = os.environ.get("POSTGRES_USER", "myappuser")
db_pass = os.environ.get("POSTGRES_PASSWORD", "myapppassword")
db_host = os.environ.get("POSTGRES_SERVICE_HOST", "localhost")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://myappuser:myapppassword@db/myappdb'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuração de teste
# Configure para usar uma base de dados de teste, e.g., SQLite in-memory
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["TESTING"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from system.infrastructure.adapters.database.models import *

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def hello():
    return "<h1>Hello, Mundo!</h1>"


if __name__ == "__main__":
    app.run()

# Importing views
from system.adapters_entrypoints.api.routes import (
    client_views,
    order_views,
    general_view,
)


# Command to create tables
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Initialized the database!")
