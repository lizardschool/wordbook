# Migrations
alembic init migrations
alembic upgrade head
alembic downgrade 18554c40c9e
alembic revision --autogenerate -m "Rename Card.list to Card.list_id"

# wordbook
~/venv_wordbook/bin/uwsgi --socket 127.0.0.1:9966 --protocol=http -w app:app --logto /home/apps/var/log/uwsgi/%n.log &
