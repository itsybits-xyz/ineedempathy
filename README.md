# I Need Empathy

An app to train a _needs consciousness_.

# Backend Development

## Mac Setup

```
brew install python3
pip3 install virtualenv virtualenvwrapper poetry
```

## Run Server

```
workon ineedempathy
poetry install
./run.sh
```

Check http://localhost:8000/

## Migrations

Create a migration using

```
alembic revision --autogenerate -m "Description."
```

Apply migration

```
alembic upgrade head
```

or

```
alembic upgrade ae10bec   # Where ae10bec is the partial sha of the version.
```

Rewind a migration

```
alembic downgrade -1  # This can also take a sha version.
```

### Seed Data

```
python3 script/seed.py
```

# Frontend Development

```
nvm use 14
cd frontend
npm install
npm start
```

Check http://localhost:3000/
