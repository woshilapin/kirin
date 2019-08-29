# Contributing



## Code guidelines

### Naive UTC datetimes

All datetimes in Kirin **must** be :
* **UTC** : datetimes are converted to UTC as soon as possible
* **naive** : no information about timezone is stored inside (making the UTC timezone implicit).  
  To have a timezone-naive datetime, its `tzinfo` attribute must be `None`.

_Why?_  
Simplest way to always manipulate the same kind of datetimes,
being able to compare them, no matter the source.  
Especially as the database does not store/provide timezone-aware datetimes.

_Where?_  
Everywhere.  
So a naive-UTC-datetime is produced right after it's read,
and timezone info is added as late as possible when needed (ex: when requesting navitia).



### Python formatting
Python source code in this project is formatted with [Black](https://black.readthedocs.io/en/stable/)
You should enable the pre-commit git hook to be sure. It's also the easier way to run black, you can simply run:
```
pre-commit run black
```
This will only update file that you changed, if you want to run it on whole project you can add `--all`:
```
pre-commit run black --all
```
Obviously you can also [install Black traditionally](https://black.readthedocs.io/en/stable/installation_and_usage.html)
But attention: it requires python 3.6+ to run.



### Git hooks
The project provides a few git hooks that you should use to prevent any issues.
These hooks are managed by [pre-commit](https://pre-commit.com/)
that you need to [install](https://pre-commit.com/#install).
Then you can install the hooks with:
```
pre-commit install
```


## Alembic database revisions

To generate a new database revision script (after an upgrade of the model.py file):
```
honcho run ./manage.py db migrate
```
This will generate a new migration file, that you can amend to your will.

:warning: To ensure safe db migrations for both upgrade (deploy) and downgrade (rollback), please make sure that:  
Kirin version `n` is able to read/write in db version `n+1` FILLED by Kirin `n+1` (it's the case on rollback)


## Roles and architecture

Kirin is split in 4 separate "components", as seen in honcho's Procfile.

#### Kirin-webservice

> Alias 'kirin' or 'web'

Its roles are:
* display the `/status`.
* provide a POST endpoint for each type of accepted realtime provider.  
  On given endpoints, the webservice receives and directly processes the feed.
  The result is then saved in db and sent to corresponding Navitia's Kraken.
  It is mainly used for COTS.
* provide a POST endpoint to ask for a full reload on a given realtime provider.  
  When a Kraken restarts it pops a rabbitmq queue and asks Kirin to provide all info in it.
  Then the webservice asks Kirin background to fulfill this task.

There can be several of these (if they are behind a load-balancer).

#### Kirin-background

> Alias 'load_realtime'

Its role is to provide all information available in db for a given provider in the rabbitmq queue, so
that Kraken can restart fully aware of realtime.

There can be several of these if the load is important.

#### Kirin-beat

> Alias 'scheduler'

Its role is to regularly publish polling jobs destined to Kirin-workers.

There is only one of these on each platform.

#### Kirin-worker

> Alias 'worker'

Its role is to poll an external location and check if new information was published.
In that case, the worker processes it, stores the result in db and sends the corresponding info to Kraken.

There can be several of these if the load is important. At least one per polled provider is recommended.


## Tests

Most tests are implemented in `/tests` directory.  
Please read [tests readme](https://github.com/CanalTP/kirin/blob/master/tests/readme.md) for more information.


## Troubleshooting

#### Retrieve processed feed

##### pgAdmin

To use pgAdmin, simply `File/add server` then enter any `name` then
`Host`, `user` and `password` used by Kirin on given platform (default kirin / kirin).  
If you use pgAdmin, you can increase massively the number of characters per column
(as the feed is big):
`File/preferences` then `Request editor/Request editor/Maximum number of characters per column`


## Release

To generate a new release:
1. merge the version you want to release into release branch (adapt script):
   ```bash
   git checkout release
   git pull
   git merge canaltp/master
   ```
2. tag and annotate the version:
   ```bash
   git tag -a <version> # then annotate with 'Version <version>'
   # check that the version is OK
   git describe # should output the desired version
   ```
3. if needed merge back release into master branch:
   ```bash
   git checkout master
   git pull
   git merge release
   ```
4. push master, release and tags to central repo
   ```bash
   git push canaltp release master --tags
   ```
