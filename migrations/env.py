import logging
from logging.config import fileConfig
import sys
import os

from alembic import context
from flask import current_app

# Ensure your app's root directory is on sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Flask app factory and the db instance
from app.main import create_app
from app.main.extensions import db

# Create Flask app instance
flask_app = create_app()

# Alembic config object for .ini access
config = context.config

# Set up logging from alembic.ini
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Use Flask app context to safely access app extensions and metadata
with flask_app.app_context():
    target_metadata = current_app.extensions['migrate'].db.metadata

    def get_engine():
        """Get SQLAlchemy engine, compatible with different Flask-Migrate versions."""
        try:
            return current_app.extensions['migrate'].db.get_engine()
        except (AttributeError, TypeError):
            return current_app.extensions['migrate'].db.engine

    def get_engine_url():
        """Return database URL with unmasked password for Alembic config."""
        try:
            return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
        except AttributeError:
            return str(get_engine().url).replace('%', '%%')

    # Set SQLAlchemy URL in Alembic config dynamically
    config.set_main_option('sqlalchemy.url', get_engine_url())

    # Migration configuration arguments from Flask-Migrate
    migrate_conf_args = current_app.extensions['migrate'].configure_args or {}

    def run_migrations_offline():
        """Run migrations without DB connection (offline mode)."""
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online():
        """Run migrations with DB connection (online mode)."""

        def process_revision_directives(context, revision, directives):
            if getattr(config.cmd_opts, 'autogenerate', False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info('No changes in schema detected.')

        # Add process_revision_directives hook if not already present
        if migrate_conf_args.get("process_revision_directives") is None:
            migrate_conf_args["process_revision_directives"] = process_revision_directives

        connectable = get_engine()

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                **migrate_conf_args,
            )

            with context.begin_transaction():
                context.run_migrations()


    # Run migration based on mode
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
