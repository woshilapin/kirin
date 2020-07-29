# Tests

## Run

To run the tests, please setup dependencies described in [main README](../readme.md#setup).
Then you can use the makefile available:

```sh
make test
```

For information, this runs py.test (after updating dependencies) in the kirin
root directory as would:

```sh
KIRIN_CONFIG_FILE=test_settings.py py.test --doctest-modules
```

## Test with a database

To be able to correctly test kirin, a database is needed.
To have a brand new database, a docker with a db is set up once for each test session.

The db scheme is resetted once per module in tests/integration.
The scheme is upgraded/downgraded for each module to test the migration scripts.

The db is cleaned up before each tests in tests/integration, so each tests are completely independent.
