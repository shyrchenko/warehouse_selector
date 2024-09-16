from pytest import fixture


@fixture
def api_host():
    return 'http://ws-api:5000/'


@fixture
def static_data_path():
    return 'tests/static/data.json'
