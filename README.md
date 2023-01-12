# Flask Starter Template
This is a starter template for a Flask Python backend that is ready for use in development and production environments with minimal to no configuration.
## Getting Started
You will need to set up a database for this web server template. Ideally, PostgreSQL or MySQL and not SQLite. You will need to have PostgreSQL/MySQL installed in order to install and run the matching Python libraries and instantiate a `db` connection.

`pip install -r requirements.txt`

## Commands

#### [Flask Migrate commands](https://flask-migrate.readthedocs.io/en/latest/)
These are the commands you'll be using the most often as you develop. I recommend you verify that your database is in the exact state you expect it to be after every step with SQL until you're reasonably certain about what's happening. Then you can move to every other step. Maybe.

```
flask db --help
flask db init
flask db current
flask db upgrade
flask db downgrade
```
## Folder structure
