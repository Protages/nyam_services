## Run server:
- `uvicorn --port=8003 src.core.main:app --reload`


## Migrations
1. Create new migration file:
`alembic revision --message="YOUR_NAME" --autogenerate`

2. Apply created migration file to db:

`alembic upgrade head`

or with migration file revision unique id:

`alembic upgrade b0c577195619`


## Onion Architecture
