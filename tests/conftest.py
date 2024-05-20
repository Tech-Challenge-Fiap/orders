from typing import Iterator
from unittest.mock import patch

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers
from flask_testing import TestCase
from app import app, db


pytest_plugins = [
    "tests.fixtures",
]


class BaseConfTest(TestCase):
    pass


class BaseRepositoryConfTest(BaseConfTest):
    def create_app(self):
        # Ensure the Flask app is set up for testing mode.
        app.config["TESTING"] = True
        return app

    def setUp(self):
        # Create all tables necessary for all tests.
        db.create_all()

    def tearDown(self):
        # Drop all tables after tests finish.
        db.session.remove()
        db.drop_all()


class BasePatchConfTest(BaseConfTest):
    @classmethod
    def tearDownClass(cls) -> None:
        patch.stopall()
        super().tearDownClass()


class BaseUseCaseConfTest(BasePatchConfTest):
    pass


class BaseRouteConfTest(BasePatchConfTest):
    flask_app = app

    @property
    def client(self) -> FlaskClient:
        """
        Fixture that creates client for requesting server.

        :param flask_app: the application.
        :yield: client for the app.
        """
        return self.flask_app.test_client()


class BaseEventConfTest(BasePatchConfTest):
    pass


@pytest.fixture
def flask_app() -> Flask:
    """
    Fixture for creating Flask app.
    :return: flask app with mocked dependencies.
    """
    return app


@pytest.fixture
def client(flask_app: Flask) -> Iterator[FlaskClient]:
    """
    Fixture that creates client for requesting server.
    :param flask_app: the application.
    :yield: client for the app.
    """
    authorization_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcGYiOiJhbm9ueW1vdXMiLCJpYXQiOjE3MTA4MTEwMjUsImV4cCI4758586MTcxMDgxNDYyNX0.Cjzev847laO0V57YyyEimjUmYi10EWOBNpkeQI_xY6c"

    with flask_app.test_client() as test_client:
        headers = Headers()
        headers.add("Authorization", f"Bearer {authorization_token}")
        test_client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {authorization_token}"
        yield test_client
