Project: Instagram analysis by Pushin Alexander



1) Launch bash script "make_virtualenv.bash" (by command "./make_virtualenv.bash" in bash)

2) Create database named "db" in mysql (Sign in mysql and type command "CREATE DATABASE db")

3) Launch python script "create_database.py" (by command "./create_database.py" in bash)


To start server launch "celery worker -A app.celery", "redis-server" (both have to start in virtualenv) and then "./start.py"
Attention: correct work is guaranted only on server (54.149.115.96)
