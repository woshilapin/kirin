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
