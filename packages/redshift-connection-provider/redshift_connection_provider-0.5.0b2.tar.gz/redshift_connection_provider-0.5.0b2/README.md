# Redshift Connection Provider

[![PyPI Latest Release](https://img.shields.io/pypi/v/redshift-connection-provider.svg)](https://pypi.org/project/redshift-connection-provider/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An opinionated class to retrieve a Redshift connection object compatible with [psycopg2](https://pypi.org/project/psycopg2/).

## Install

```sh
pip install redshift-connection-provider
```

## Usage

```py
# Import
import os
import psycopg2
from redshift_connection.provider import RSConnectionProvider
# Initialize Class
rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID)
# Or via ENV Variable
os.environ["CLUSTER_ID"] = CLUSTER_ID
rs_conn = RSConnectionProvider()
# Create connection dict
conn_object = rs_conn.get_conn()
# Pass it to psycopg2 to create a connection
conn = psycopg2.connect(**conn_object)
```

## Connection Parameters:

- Database User: Can be set via parameter upon class init, as an environment variable (`DB_USER`), stored as a secret in AWS Secret Manager (specify secret name as environment variable `DB_USER_SECRET_NAME`); if none is set master user will be used.
- Database Name: Can be set via parameter upon class init or as an environment variable (`DB_NAME`).
- Database Password: Can be set as an environment variable (`DB_PASS`), stored as a secret in AWS Secret Manager (specify secret name as environment variable `DB_PASS_SECRET_NAME`); if none is set, a temporary password is acquired using AWS APIs. The temporary password will be scoped to the user specified (which can be auto-created) and to the database passed (if any).
- Database Host: Acquired automatically via AWS APIs using provided `CLUSTER_ID`.
- Database Port: Acquired automatically via AWS APIs using provided `CLUSTER_ID`.

## License

[MIT](https://github.com/dreamorosi/redshift-connection-provider/blob/main/LICENSE)

## Contributing & Developing

PRs are welcome as long as documented, accompained by passing unit tests and in scope with the project.

To setup the development environment run:

```sh
pipenv install --dev
```

or manually install all the development dependencies found in the [Pipfile](https://github.com/dreamorosi/redshift-connection-provider/blob/main/Pipfile).
