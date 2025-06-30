from pytest import fixture


@fixture
def mock_do_auth():
    """
    Mocando o do_auth
    """
    from app.api.common.auth_handler import do_auth
    from app.api_main import app

    app.dependency_overrides[do_auth] = lambda: None
    yield
    # Limpando o override
    app.dependency_overrides[do_auth] = {}
