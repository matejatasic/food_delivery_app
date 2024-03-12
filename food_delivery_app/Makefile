.PHONY: run
run:
	python3 manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000

migrate:
	python3 manage.py migrate

seed:
	python3 manage.py seed --mode=refresh

