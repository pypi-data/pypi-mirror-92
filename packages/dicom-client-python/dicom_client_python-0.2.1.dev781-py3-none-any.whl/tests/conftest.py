from os import environ


def pytest_addoption(parser):
    parser.addoption("--blob_conn", default=environ.get("AZURE_STORAGE_CONNECTION_STRING"))
    parser.addoption("--sql_conn", default=environ.get("SQL_CONNECTION_STRING"))
    parser.addoption("--dcm_host", default=environ.get("DCM_HOST"))
    parser.addoption("--aad_authority", default=environ.get("AUTHORITY"))
    parser.addoption("--client_id", default=environ.get("CLIENT_ID"))
    parser.addoption("--client_secret", default=environ.get("CLIENT_SECRET"))
    parser.addoption("--oauth_resource", default=environ.get("OAUTH_RESOURCE"))
    parser.addoption("--table_prefix", default=environ.get("TABLE_PREFIX"))
