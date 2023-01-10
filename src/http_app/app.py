from sanic import Sanic
from sanic.log import logger
from sanic_openapi import openapi3_blueprint

from src.settings import Settings
from src.http_app.routes import routes_blueprint
from src.http_app.app_entety import AppConfig
from src.repositories.init_repositories import Repositories


def create_app(settings: Settings = None) -> Sanic:
    if settings is None:
        settings = Settings.instantiate()

    repositories = Repositories.instantiate(
        settings=settings,
        logger=logger,
    )

    app = Sanic(
        "UserSuspicionRateAnalyzer",
        log_config=settings.logging,
        config=AppConfig(
            settings=settings,
            repositories=repositories,
        ),
    )
    app.blueprint(routes_blueprint)
    app.blueprint(openapi3_blueprint)

    return app
