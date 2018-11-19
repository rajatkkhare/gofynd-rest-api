from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from gofynd.api.resources import api_bp
import click

db = SQLAlchemy()
api = Api(api_bp)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py')

    @app.before_first_request
    def create_tables():
        db.create_all()

    register_libraries(app)
    register_blueprints(app)
    register_cli_command(app)
    register_api_resources()

    return app


def register_libraries(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')


def register_api_resources():
    from gofynd.api.resources.Auth import Auth
    api.add_resource(Auth, '/auth/<string:action>')
    from gofynd.api.resources.admin.ImportData import ImportData
    api.add_resource(ImportData, '/admin/import_data')
    from gofynd.api.resources.admin.Movies import Movies
    api.add_resource(Movies, '/admin/movies')
    from gofynd.api.resources.admin.Movie import Movie
    api.add_resource(Movie, '/admin/movie/<int:movie_id>')
    from gofynd.api.resources.front.Movies import Movies
    api.add_resource(Movies, '/movies', endpoint='/movies')


def register_cli_command(app):
    from gofynd.models.User import User

    @app.cli.command()
    def createsuperuser():
        first_name = click.prompt('First name', type=str)
        last_name = click.prompt('Last name', type=str)
        email = click.prompt('Email', type=str, value_proc=validate_email)
        password = click.prompt('Password', type=str, hide_input=True, confirmation_prompt=True,
                                value_proc=validate_password)
        u = User(email, password, first_name, last_name)
        u.is_active = 1
        u.is_super = 1
        u.is_admin = 1
        click.echo('Super user created successfully.') if u.save() else click.echo('Error! Try again.')

    @app.cli.command()
    def change_password():
        email = click.prompt('Email', type=str, value_proc=email_exist)
        password = click.prompt('Password', type=str, hide_input=True, confirmation_prompt=True,
                                value_proc=validate_password)
        u = User.query.filter_by(email=email).first()
        u.password = password
        u.set_password()
        click.echo('Password changed successfully.') if u.save() else click.echo('Error! Try again.')

    def validate_password(value):
        if len(value) < 5:
            raise click.BadParameter('Password must be at least 5 characters long.')
        return value

    def validate_email(value):
        if User.query.filter_by(email=value).count():
            raise click.BadParameter('Email already used.')
        return value

    def email_exist(value):
        if not User.query.filter_by(email=value).count():
            raise click.BadParameter('User not found.')
        return value
