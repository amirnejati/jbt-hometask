# alembic  revision --autogenerate -m "change name"
alembic upgrade head
uvicorn main:app --reload

