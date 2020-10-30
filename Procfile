web: KIRIN_USE_GEVENT=true FLASK_DEBUG=1 FLASK_APP=kirin:app flask run -p 54746 --without-threads
load_realtime: KIRIN_USE_GEVENT=true ./manage.py load_realtime
worker: celery worker -A kirin.tasks.celery -c 3
scheduler: celery beat -A kirin.tasks.celery
piv_worker: KIRIN_USE_GEVENT=true ./manage.py piv_worker
