from sanic import Sanic
from sanic import Request as SanicRequest
from sanic.config import Config

from src.settings import Settings
from src.repositories.init_repositories import Repositories


class AppConfig(Config):
    def __init__(
        self,
        settings: Settings,
        repositories: Repositories,
    ):
        super().__init__()
        self.settings = settings
        self.repositories = repositories


class App(Sanic):
    config: AppConfig


class Request(SanicRequest):
    app: App
