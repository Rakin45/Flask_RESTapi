import pytest
from webapp import create_app, db 



@pytest.fixture()
def flask_app():
    app = create_app("sqlite://")

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def client(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()