from sanic import Sanic
from environs import Env
from sanic.worker.loader import AppLoader

from src.http_app.app import create_app
from src.http_app.app_entety import App


def read_env_file():
    env = Env()
    env.read_env()


def set_open_api_settings():
    app.config.API_VERSION = "1.0.0"
    app.config.API_TITLE = "Car API"
    app.config.API_CONTACT_EMAIL = "abloyxob@gmail.com"
    app.config.API_DESCRIPTION = "Analyze id and ban service"


read_env_file()
loader = AppLoader(factory=create_app)
app: App = loader.load()
app.prepare(
    host=app.config.settings.application.host,
    port=app.config.settings.application.port,
    debug=True,
    access_log=True,
)
Sanic.serve(primary=app, app_loader=loader)
