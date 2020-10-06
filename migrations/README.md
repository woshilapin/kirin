# Generic single-database configuration

The database schema is maintained using [alembic] and migration files you can
find in `kirin/migrations/versions`. They each contain an `upgrade()` and a
`downgrade()` function.

To set up or upgrade your DB to the latest version of the model, you can use the
following command.

```sh
honcho run ./manage.py db upgrade
```

## Alembic database revisions

To generate a new database revision script, first edit `kirin/core/model.py` to
modify the model as you like. Then generate the migration file automatically
with the following command.

```sh
honcho run ./manage.py db migrate
```

This new generated migration file can be amended at will (see other migrations
files).

:bulb: Keep in mind that db upgrade is done **before** deployment of Kirin (and
Kirin must work all the way).\
Also, where Kirin is duplicated, at some point both Kirin version `n-1` and
Kirin version `n` are running, using the same upgraded database.

:warning: To ensure safe db migrations for both upgrade (deploy) and downgrade
(rollback), please make sure that:\
Kirin version `n` is able to read/write in db version `n+1` FILLED by Kirin
`n+1` (it's the case on rollback).\
As for a (column) removal, one should ensure that version `n-1` (and of course
`n`) don't use (read or write) the "object" removed from db. So first (in
version `n-1`) do a PR removing **any** use in python (especially in model.py)
but keeping db almost as-is, with just a "nullable" migration if needed.

[alembic]: https://pypi.org/project/alembic/
